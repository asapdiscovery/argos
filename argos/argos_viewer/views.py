from django.shortcuts import redirect, render
from .models import PDBFile
from .forms import DocumentForm
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views import generic
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page


from asapdiscovery.data.openeye import load_openeye_pdb
from asapdiscovery.data.schema_v2.complex import Complex
from asapdiscovery.dataviz.html_viz import HTMLVisualizer
import tempfile

def index(request):
    context = {}
    return render(request, "index.html", context)


def upload_file(request):
    message = "Upload as many files as you want!"
    # Handle file upload
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES["pdb_file"]
            newfile = PDBFile(pdb_file=uploaded_file)
            newfile.save()
            # Redirect to the document list after POST
            return redirect("detail",  newfile.id)
        else:
            message = "The form is not valid. Fix the following error:"
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    pdb_files = PDBFile.objects.all()

    # Render list page with the documents and the form
    context = {"pdb_files": pdb_files, "form": form, "message": message}
    return render(request, "list.html", context)



def upload_sucessful(request):
    message = "upload worked!"
    return HttpResponse(message)


class PDBListView(generic.ListView):
    model = PDBFile


@cache_page(60*60) # cache for one hour
def pdb_detail_view(request, pk):
    # Retrieve the object based on its primary key (pk)
    obj = get_object_or_404(PDBFile, pk=pk)
    data = obj.pdb_file.read()

    c = Complex.from_pdb(
        obj.pdb_file.path,
        ligand_kwargs={"compound_name": "unknown"},
        target_kwargs={"target_name": "unknown"},
    )

    tf = tempfile.NamedTemporaryFile()  
    html_viz = HTMLVisualizer(
        [c.ligand.to_oemol()], [tf], "SARS-CoV-2-Mpro", c.target.to_oemol(), color_method="fitness"
    )
    html = html_viz.make_poses_html()[0]
    return HttpResponse(html)
