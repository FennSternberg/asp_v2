from django import forms
from .models import AnalysisDetail, ThermoformingCavityParameters, ThermoformingSimulation
from django.contrib.auth.models import User
from django_select2.forms import Select2Widget
from django.core.exceptions import ValidationError

# will not be needed when transitioned to vue
def validate_positive(value):
    if value <= 0:
        raise ValidationError("The value must be a positive number.")
    
class AnalysisDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AnalysisDetailForm, self).__init__(*args, **kwargs)
        
        if user and user.is_authenticated:
            self.fields['internal_contact'].initial = user.id
    class Meta:
        model = AnalysisDetail
        fields = ['jobname', 'customer', 'internal_contact']
        widgets = {
            'jobname': forms.TextInput(attrs={'class':'form-control',  'v-model': 'formData.jobname'}),
            'customer': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Customer - Location', 'v-model': 'formData.customer'}),
        }

    internal_contact = forms.ModelChoiceField(
        queryset=User.objects.all(),
        to_field_name="id",
        label='Internal Contact',
        empty_label="Select Internal Contact",
        widget=Select2Widget(attrs={'class': 'form-control', 'v-model': 'formData.internal_contact'})
    )


class ThermoformingParametersForm(forms.ModelForm):
    w = forms.FloatField(validators=[validate_positive], widget=forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'formData.w'}))
    c1 = forms.FloatField(validators=[validate_positive], widget=forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'formData.c1'}))
    l = forms.FloatField(validators=[validate_positive], widget=forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'formData.l'}))
    c2 = forms.FloatField(validators=[validate_positive], widget=forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'formData.c2'}))
    depth = forms.FloatField(validators=[validate_positive], widget=forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'formData.depth'}))
    wall_angle = forms.FloatField(validators=[validate_positive], widget=forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'formData.wall_angle'}))
    r = forms.FloatField(validators=[validate_positive], widget=forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'formData.r'}))
    rb = forms.FloatField(validators=[validate_positive], widget=forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'formData.rb'}))
    rf = forms.FloatField(validators=[validate_positive], widget=forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'formData.rf'}))

    class Meta:
        model = ThermoformingCavityParameters
        fields = '__all__'
        widgets = {
            'shape': forms.RadioSelect(attrs={'class': 'form-control', 'v-model': 'formData.shape'}),
            'profile': forms.RadioSelect(attrs={'class': 'form-control', 'v-model': 'formData.profile'}),
            'laminate_material': forms.Select(attrs={'class': 'form-control', 'v-model': 'formData.laminate_material'}),
            'lid_material': forms.Select(attrs={'class': 'form-control', 'v-model': 'formData.lid_material'}),
            'contact': forms.Select(attrs={'class': 'form-control', 'v-model': 'formData.contact'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'formData.temperature'}),
            'pressure': forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'formData.pressure'}),
            'pressure_build_up_time': forms.NumberInput(attrs={'class': 'form-control', 'v-model': 'formData.pressure_build_up_time'}),
        }

class ThermoformingVerificationSimulationForm(forms.ModelForm):
    class Meta:
        model = ThermoformingSimulation
        fields = ['calculate_permeability', 'compare_with_other_laminates_and_lids']
        widgets = {
            'calculate_permeability': forms.CheckboxInput(attrs={'class': 'form-check-input', 'v-model': 'formData.calculate_permeability'}),
            'compare_with_other_laminates_and_lids': forms.CheckboxInput(attrs={'class': 'form-check-input', 'v-model': 'formData.compare_with_other_laminates_and_lids'}),
        }

