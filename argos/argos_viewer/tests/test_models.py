from django.test import TestCase
from argos_viewer.models import PDBFile, TargetPDBFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
import os

class PDBFileModelTest(TestCase):
    def setUp(self):
        self.file = SimpleUploadedFile("test.pdb", b"pdb file content")
        self.pdb_file = PDBFile.objects.create(file=self.file)


    def test_pdb_file_created(self):
        self.assertTrue(os.path.exists(self.pdb_file.file.path))

    def test_file_extension(self):
        self.assertEqual(self.pdb_file.file.name.split(".")[-1], "pdb")

class TargetPDBFileModelTest(TestCase):
    def setUp(self):
        self.file = SimpleUploadedFile("test.pdb", b"pdb file content")
        self.pdb_file = PDBFile.objects.create(file=self.file)
        self.target_pdb_file = TargetPDBFile.objects.create(pdb_file=self.pdb_file, target="test_target", upload_date=timezone.now())

    def tearDown(self):
        if os.path.exists(self.target_pdb_file.pdb_file.file.path):
            os.remove(self.target_pdb_file.pdb_file.file.path)

    def test_target_pdb_file_created(self):
        self.assertTrue(TargetPDBFile.objects.exists())

    def test_target(self):
        self.assertEqual(self.target_pdb_file.target, "test_target")

    def test_upload_date(self):
        self.assertIsNotNone(self.target_pdb_file.upload_date)

    def test_pdb_file_deletion_on_target_pdb_file_deletion(self):
        self.target_pdb_file.delete()
        self.assertFalse(os.path.exists(self.pdb_file.file.path))



