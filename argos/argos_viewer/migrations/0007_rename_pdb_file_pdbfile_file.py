# Generated by Django 4.2.7 on 2023-11-29 03:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('argos_viewer', '0006_remove_pdbfile_upload_date_targetpdbfile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pdbfile',
            old_name='pdb_file',
            new_name='file',
        ),
    ]
