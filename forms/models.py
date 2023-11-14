from django.db import models
from django.contrib.auth.models import User
from material_data.models import LayerStructure

class AnalysisDetail(models.Model):
    # ID of the user making the request
    user = models.ForeignKey(User, related_name='analysis_requests', on_delete=models.CASCADE)
    internal_contact = models.ForeignKey(User, related_name='internal_contact_for', on_delete=models.CASCADE)
    jobname = models.CharField(max_length=255)
    customer = models.CharField(max_length=255)
    ANALYSIS_TYPE_CHOICES = [
        ('general', 'General'),
        ('thermoforming_verification', 'Thermoforming Verification'),
    ]
    analysis_type = models.CharField(
        max_length=30,
        choices=ANALYSIS_TYPE_CHOICES,
        default='general',
    )

    requested_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    STATUS_CHOICES = [
        ('saved','Saved'),
        ('submitted', 'Submitted'),
        ('completed', 'Completed'),
        ('simulating', 'Simulating'),
        ('aborted', 'Aborted'),
        ('rejected','Rejected')
    ]
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='saved',
    )
    
    reviewer = models.ForeignKey(User, related_name='reviewed_analysis', null=True, blank=True, on_delete=models.SET_NULL)
    report_name = models.CharField(max_length=255, null=True, blank=True)

class ThermoformingCavityParameters(models.Model):
    # Cavity Geometry Fields
    SHAPE_CHOICES = [('round', 'Round'), ('oblong', 'Oblong')]
    PROFILE_CHOICES = [('profile1', 'Profile 1'), ('profile2', 'Profile 2'), ('profile3', 'Profile 3')]
    
    shape = models.CharField(max_length=10, choices=SHAPE_CHOICES, default='round')
    profile = models.CharField(max_length=10, choices=PROFILE_CHOICES, default='profile1')
    w = models.FloatField()
    c1 = models.FloatField()
    l = models.FloatField()
    c2 = models.FloatField() 
    depth = models.FloatField()
    wall_angle = models.FloatField()
    r = models.FloatField()
    rb = models.FloatField() 
    rf = models.FloatField()

    def get_shape_choices(self):
        return [
              {
          "label": "Round",
          "value": "round",
          "path": "/static/images/cavity/round.png?v=2",
        },
        {
          "label": "Oblong",
          "value": "oblong",
          "path": "/static/images/cavity/oblong.png?v=2",
        }
        ]
    
    def get_profile_choices(self):
        return [
              {
          "label": "Profile 2",
          "value": "profile2",
          "path": "/static/images/cavity/profile2.png?v=2",
        },
        {
          "label": "Profile 3",
          "value": "profile3",
          "path": "/static/images/cavity/profile3.png?v=2",
        },
        ]
     
class ThermoformingProcessParameters(models.Model):
    CONTACT_CHOICES = [('kinematic', 'Kinematic'), ('penalty', 'Penalty')]
    contact = models.CharField(max_length=20, choices=CONTACT_CHOICES, default='kinematic')
    temperature = models.FloatField(default=125)
    pressure = models.FloatField(default=1)
    pressure_build_up_time = models.FloatField(default=0.05)

class ThermoformingPlugParameters(models.Model):
    width = models.FloatField()
    length = models.FloatField()
    range_min = models.FloatField()
    range_max = models.FloatField()
    n_travel = models.FloatField()
    r_b = models.FloatField()
    r_f = models.FloatField()

class ThermoformingSimulation(models.Model):
    analysis_detail = models.ForeignKey(AnalysisDetail, on_delete=models.CASCADE)
    cavity_parameters = models.ForeignKey(ThermoformingCavityParameters, on_delete=models.SET_NULL, null=True, default=None)
    process_parameters = models.ForeignKey(ThermoformingProcessParameters, on_delete=models.SET_NULL, null=True, default=None)
    plug_parameters = models.ForeignKey(ThermoformingPlugParameters, on_delete=models.SET_NULL, null=True, default=None)
    cavity_materials = models.ManyToManyField(LayerStructure, related_name="cavity_materials")
    lid_materials = models.ManyToManyField(LayerStructure, related_name="lid_materials")