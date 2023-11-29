from .views import home, upload_sucessful, TargetPDBListView, target_pdb_detail_view, failed
from django.urls import path, include


urlpatterns = [
    path('', home, name='home'),
    path('upload_sucessful', upload_sucessful,  name='upload_sucessful'),
    path('pdb_files', TargetPDBListView.as_view(), name='pdb_files'),
    path('pdb_file/<int:pk>', target_pdb_detail_view, name='detail'),
    path('failed', failed, name='failed'),
]
