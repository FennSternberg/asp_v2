# Generated by Django 4.2.4 on 2023-10-30 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material_data', '0021_otrdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='thermoformingdata',
            name='otr_data',
            field=models.ManyToManyField(to='material_data.otrdata'),
        ),
    ]