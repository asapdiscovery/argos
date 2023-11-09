from .views import upload_file, upload_sucessful, PDBListView, pdb_detail_view
from django.urls import path, include


urlpatterns = [
    path('', upload_file, name='upload_file'),
    path('upload_sucessful', upload_sucessful,  name='upload_sucessful'),
    path('pdb_files', PDBListView.as_view(), name='pdb_files'),
    path('pdb_file/<int:pk>', pdb_detail_view, name='detail'),
]
