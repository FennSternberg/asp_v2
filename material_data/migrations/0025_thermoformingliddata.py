# Generated by Django 4.2.4 on 2023-10-30 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('material_data', '0024_druckerpragercurvedata_direction'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThermoformingLidData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='thermoforminglid_data', to='material_data.material')),
                ('otr_data', models.ManyToManyField(to='material_data.otrdata')),
                ('wvtr_data', models.ManyToManyField(to='material_data.wvtrdata')),
            ],
        ),
    ]