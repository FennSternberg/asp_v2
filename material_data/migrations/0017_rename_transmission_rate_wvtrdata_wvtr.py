# Generated by Django 4.2.4 on 2023-10-25 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('material_data', '0016_wvtrdata_remove_thermoformingdata_permeability_data_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wvtrdata',
            old_name='transmission_rate',
            new_name='WVTR',
        ),
    ]