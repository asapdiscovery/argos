from django import forms
from django.core.exceptions import ValidationError
import codecs
from pathlib import Path

def validate_pdb_extn(value):
    if not Path(value.name).suffix == ".pdb":
        raise ValidationError('Invalid file, must upload PDB file')


def is_utf8_file(value):
    try:
        value.read().decode('utf-8')
    except UnicodeDecodeError:
        raise ValidationError("File is not UTF8")


class DocumentForm(forms.Form):
    pdb_file = forms.FileField(label='Select a file', validators=[validate_pdb_extn, is_utf8_file])

    