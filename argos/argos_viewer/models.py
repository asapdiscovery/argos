from django.db import models
from django.core.validators import FileExtensionValidator


class PDBFile(models.Model):
    file = models.FileField(validators=[FileExtensionValidator(['pdb'])], upload_to="pdb_data")


class TargetPDBFile(models.Model):
    pdb_file = models.ForeignKey(PDBFile, on_delete=models.CASCADE)
    target = models.CharField(max_length=200)
    upload_date = models.DateTimeField(auto_now_add=True)
