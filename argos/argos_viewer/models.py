from django.db import models
from django.core.validators import FileExtensionValidator


class PDBFile(models.Model):
    pdb_file = models.FileField(validators=[FileExtensionValidator(['pdb'])], upload_to="pdb_data")