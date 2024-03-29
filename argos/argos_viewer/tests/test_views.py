from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from argos_viewer.models import PDBFile, TargetPDBFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.contrib.auth.models import User
from asapdiscovery.data.testing.test_resources import fetch_test_file


class ViewTests(TestCase):
    def setUp(self):
        self._test_file = fetch_test_file("Mpro-P2660_0A_bound.pdb")
        with open(self._test_file, "r") as f:
            self._file_contents = f.read()
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.file = SimpleUploadedFile("test.pdb", self._file_contents.encode())
        self.pdb_file = PDBFile.objects.create(file=self.file)
        self.target_pdb_file = TargetPDBFile.objects.create(pdb_file=self.pdb_file, target="SARS-CoV-2-Mpro", upload_date=timezone.now())

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)  # Redirects to home

    def test_home_view_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'argos_viewer/home.html')

    def test_upload_successful_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('upload_sucessful'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'upload worked!')


    def test_target_pdb_detail_view_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('detail', args=[self.target_pdb_file.pk]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_failed_view_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('failed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'argos_viewer/failed.html')

    def test_no_fitness_data_view_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('no_fitness_data', args=['target_name']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'argos_viewer/no_fitness_data.html')

    # Add tests for POST requests as well if necessary
