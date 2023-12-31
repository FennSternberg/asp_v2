# Generated by Django 4.2.4 on 2023-11-03 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0005_alter_thermoformingverificationsimulation_cavity_materials_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThermoformingPlugParameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.FloatField()),
                ('range_min', models.FloatField()),
                ('range_max', models.FloatField()),
                ('n_travel', models.FloatField()),
                ('r_b', models.FloatField()),
                ('r_f', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='thermoformingverificationsimulation',
            name='thermoforming_plug_parameters',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forms.thermoformingplugparameters'),
        ),
    ]
