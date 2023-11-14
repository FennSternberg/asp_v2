# Generated by Django 4.2.4 on 2023-11-03 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0002_alter_thermoformingverificationsimulation_thermoforming_cavity_parameters_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thermoformingprocessparameters',
            name='laminate_material',
        ),
        migrations.RemoveField(
            model_name='thermoformingprocessparameters',
            name='lid_material',
        ),
        migrations.RemoveField(
            model_name='thermoformingverificationsimulation',
            name='calculate_permeability',
        ),
        migrations.RemoveField(
            model_name='thermoformingverificationsimulation',
            name='compare_with_other_laminates_and_lids',
        ),
        migrations.AlterField(
            model_name='analysisdetail',
            name='analysis_type',
            field=models.CharField(choices=[('general', 'General'), ('thermoforming_verification', 'Thermoforming Verification')], default='general', max_length=30),
        ),
    ]