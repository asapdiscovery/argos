from django.shortcuts import redirect, render
from .models import PDBFile, TargetPDBFile
from .forms import DocumentForm
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views import generic
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required


from asapdiscovery.data.openeye import load_openeye_pdb
from asapdiscovery.data.schema_v2.complex import Complex
from asapdiscovery.dataviz.html_viz import HTMLVisualizer
import tempfile

def index(request):
    context = {}
    return redirect("home")

@login_required
def home(request):
    message = ""
    # Handle file upload
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES["pdb_file"]
            pdb_file_instance = PDBFile(pdb_file=uploaded_file)
            pdb_file_instance.save()
            target = form.cleaned_data["dropdown_menu"]

            target_pdb = TargetPDBFile(pdb_file=pdb_file_instance, target=target)
            target_pdb.save()
            # Redirect to the document list after POST
            return redirect("detail",  target_pdb.id)
        else:
            message = "The form is not valid. Fix the following error:"
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    latest_5 = TargetPDBFile.objects.order_by("-upload_date")[:5]

    # Render list page with the documents and the form
    context = {"target_pdb_file": latest_5, "form": form, "message": message}
    return render(request, "argos_viewer/home.html", context)


@login_required
def upload_sucessful(request):
    message = "upload worked!"
    return HttpResponse(message)

class TargetPDBListView(generic.ListView):
    model = TargetPDBFile

@login_required
@cache_page(60*60) # cache for one hour
def target_pdb_detail_view(request, pk):
    # Retrieve the object based on its primary key (pk)
    obj = get_object_or_404(TargetPDBFile, pk=pk)
    data = obj.pdb_file.file.read()

    try:
        c = Complex.from_pdb(
            obj.pdb_file.file.path,
            ligand_kwargs={"compound_name": "unknown"},
            target_kwargs={"target_name": "unknown"},
        )

        tf = tempfile.NamedTemporaryFile()  
        html_viz = HTMLVisualizer(
            [c.ligand.to_oemol()], [tf], obj.target, c.target.to_oemol(), color_method="fitness"
        )
        html = html_viz.make_poses_html()[0]
    except:
        redirect("failed")

    return HttpResponse(html)

@login_required
def failed(request):
    return render(request, "argos_viewer/failed.html")
