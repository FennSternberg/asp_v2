from django.db import models
from django.contrib.auth.models import User

class AnalysisDetail(models.Model):
    # ID of the user making the request
    user = models.ForeignKey(User, related_name='analysis_requests', on_delete=models.CASCADE)
    internal_contact = models.ForeignKey(User, related_name='internal_contact_for', on_delete=models.CASCADE)
    jobname = models.CharField(max_length=255)
    customer = models.CharField(max_length=255)
    ANALYSIS_TYPE_CHOICES = [
        ('general', 'General'),
        ('thermoforming_verification', 'Thermoforming Verification'),
        ('thermoforming_plug', 'Thermoforming Plug'),
        ('thermoforming_cad', 'Thermoforming CAD'),
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
     
class ThermoformingProcessParameters(models.Model):
    # Thermoforming Material Fields
    LAMINATE_CHOICES = [("amsky_305","Amsky 305")]
    LID_CHOICES = [("amsky_70","Amsky lid 70")]
    
    laminate_material = models.CharField(max_length=50, choices=LAMINATE_CHOICES)
    lid_material = models.CharField(max_length=50, choices=LID_CHOICES)
    
    # Admin Usage Parameters Fields
    CONTACT_CHOICES = [('kinematic', 'Kinematic'), ('penalty', 'Penalty')] 
    
    contact = models.CharField(max_length=20, choices=CONTACT_CHOICES, default='kinematic')
    temperature = models.FloatField(default=125)
    pressure = models.FloatField(default=1)
    pressure_build_up_time = models.FloatField(default=0.05)


class ThermoformingVerificationSimulation(models.Model):
    analysis_detail = models.ForeignKey(AnalysisDetail, on_delete=models.CASCADE)
    thermoforming_cavity_parameters = models.ForeignKey(ThermoformingCavityParameters, on_delete=models.SET_NULL, null=True, default=None)
    thermoforming_process_parameters = models.ForeignKey(ThermoformingProcessParameters, on_delete=models.SET_NULL, null=True, default=None)
    calculate_permeability = models.BooleanField(default=False)
    compare_with_other_laminates_and_lids = models.BooleanField(default=False)

