# Generated by Django 4.2.4 on 2023-10-25 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('material_data', '0008_rename_laminate_layerstructureorder_layer_structure_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LayerStructureOrder',
            new_name='MaterialOrder',
        ),
    ]
