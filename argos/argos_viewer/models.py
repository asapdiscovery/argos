from typing import Any
from django.db import models
from django.core.validators import FileExtensionValidator
import os

class PDBFile(models.Model):
    file = models.FileField(validators=[FileExtensionValidator(['pdb'])], upload_to="pdb_data")

    def delete(self, *args, **kwargs):
        # Delete the file when the instance is deleted
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super(PDBFile, self).delete(*args, **kwargs)

class TargetPDBFile(models.Model):
    pdb_file = models.ForeignKey(PDBFile, on_delete=models.CASCADE)
    target = models.CharField(max_length=200)
    upload_date = models.DateTimeField(auto_now_add=True)


    def delete(self, *args, **kwargs):
        # Delete the associated PDBFile instance, which should trigger its delete method
        if self.pdb_file:
            self.pdb_file.delete()
        super(TargetPDBFile, self).delete(*args, **kwargs)