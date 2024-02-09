from django.test import TestCase, Client
from django.urls import reverse
from argos_viewer.models import PDBFile, TargetPDBFile
from django.contrib.auth.models import User


class ViewTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')

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

    # You can write similar tests for other views...

    def test_target_pdb_detail_view_GET(self):
        self.client.force_login(self.user)
        target_pdb = TargetPDBFile.objects.create()
        response = self.client.get(reverse('detail', args=[target_pdb.pk]))
        self.assertEqual(response.status_code, 200)
        # Make assertions based on the response content or template used

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
