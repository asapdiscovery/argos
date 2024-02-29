from django import forms
from django.core.exceptions import ValidationError
import codecs
from pathlib import Path
from asapdiscovery.data.services.postera.manifold_data_validation import TargetTags


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
    options = list(zip(TargetTags.get_values(), TargetTags.get_values()))
    dropdown_menu = forms.ChoiceField(choices=options, label='Select a Target')
    
