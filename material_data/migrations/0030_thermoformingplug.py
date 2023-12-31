# Generated by Django 4.2.4 on 2023-11-07 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material_data', '0029_layerstructure_released_for_thermoforming_lid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThermoformingPlug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('friction_coefficient', models.FloatField()),
            ],
        ),
    ]
