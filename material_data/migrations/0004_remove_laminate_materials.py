# Generated by Django 4.2.4 on 2023-10-24 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('material_data', '0003_laminate_laminatematerial_laminate_materials'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laminate',
            name='materials',
        ),
    ]
