from django.shortcuts import redirect, render
from .models import PDBFile, TargetPDBFile
from .forms import DocumentForm
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required


from asapdiscovery.data.schema.complex import Complex
from asapdiscovery.dataviz.html_viz import HTMLVisualizer
from asapdiscovery.genetics.fitness import target_has_fitness_data

import logging

logger = logging.getLogger("django")


def index(request):
    return redirect("home")


@login_required
def home(request):
    message = ""
    # Handle file upload
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES["pdb_file"]
            pdb_file_instance = PDBFile(file=uploaded_file)
            pdb_file_instance.save()
            target = form.cleaned_data["dropdown_menu"]

            target_pdb = TargetPDBFile(pdb_file=pdb_file_instance, target=target)
            target_pdb.save()
            # Redirect to the document list after POST
            return redirect("detail", target_pdb.id)
        else:
            message = "The form is not valid. Fix the following error:"
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    latest_5 = TargetPDBFile.objects.order_by("-upload_date")[:5]

    # Render list page with the documents and the form
    context = {"target_pdbs": latest_5, "form": form, "message": message}
    return render(request, "argos_viewer/home.html", context)


@login_required
def upload_sucessful(request):
    message = "upload worked!"
    return HttpResponse(message)


class TargetPDBListView(generic.ListView):
    model = TargetPDBFile


@login_required
@cache_page(60 * 60)  # cache for one hour
def target_pdb_detail_view(request, pk):
    # Retrieve the object based on its primary key (pk)
    obj = get_object_or_404(TargetPDBFile, pk=pk)
    data = obj.pdb_file.file.read()

    if not target_has_fitness_data(obj.target):
        return redirect("no_fitness_data", obj.target)

    try:
        c = Complex.from_pdb(
            obj.pdb_file.file.path,
            ligand_kwargs={"compound_name": "unknown"},
            target_kwargs={"target_name": "unknown"},
        )

        html_viz = HTMLVisualizer(
            target=obj.target, colour_method="fitness", write_to_disk=False, align=True
        )
        html = html_viz.visualize(inputs=[c])[0]
        logger.debug("Made pose html")
    except Exception as e:
        logger.error(f"rendering failed with exception {e}")
        return redirect("failed")

    return HttpResponse(html)


@login_required
def failed(request):
    return render(request, "argos_viewer/failed.html")


@login_required
def no_fitness_data(request, target):
    context = {"target": target}
    return render(request, "argos_viewer/no_fitness_data.html", context)
