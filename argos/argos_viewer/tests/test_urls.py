from django.test import SimpleTestCase
from django.urls import reverse, resolve
from argos_viewer.views import home, upload_sucessful, TargetPDBListView, target_pdb_detail_view, failed, no_fitness_data

class TestUrls(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_upload_sucessful_url_resolves(self):
        url = reverse('upload_sucessful')
        self.assertEqual(resolve(url).func, upload_sucessful)

    def test_pdb_files_url_resolves(self):
        url = reverse('pdb_files')
        self.assertEqual(resolve(url).func.view_class, TargetPDBListView)

    def test_detail_url_resolves(self):
        url = reverse('detail', args=[1])  # assuming pk=1
        self.assertEqual(resolve(url).func, target_pdb_detail_view)

    def test_failed_url_resolves(self):
        url = reverse('failed')
        self.assertEqual(resolve(url).func, failed)

    def test_no_fitness_data_url_resolves(self):
        url = reverse('no_fitness_data', args=['target_name'])
        self.assertEqual(resolve(url).func, no_fitness_data)
