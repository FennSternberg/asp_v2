# Generated by Django 4.2.4 on 2023-10-25 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('material_data', '0015_remove_permeabilitydata_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='WVTRData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField()),
                ('RH', models.FloatField()),
                ('transmission_rate', models.FloatField()),
                ('diffusivity', models.FloatField(default=None, null=True)),
                ('solubility', models.FloatField(default=None, null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wvtr_data', to='material_data.material')),
            ],
        ),
        migrations.RemoveField(
            model_name='thermoformingdata',
            name='permeability_data',
        ),
        migrations.DeleteModel(
            name='PermeabilityData',
        ),
        migrations.AddField(
            model_name='thermoformingdata',
            name='wvtr_data',
            field=models.ManyToManyField(to='material_data.wvtrdata'),
        ),
    ]
