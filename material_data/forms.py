from django import forms
from .models import  ColdformingStamp, LayerStructure, Material, DensityData, OTRData, WVTRData,ColdformingData, ThermoformingData, ThermoformingLidData, YoungsModulusData,  TensileCurveData, DruckerPragerCurveData

FORM_CONTROL_ATTRS = {'class': 'form-control'}
FORM_CHECK_INPUT_ATTRS = {'class': 'form-check-input'}
FORM_CONTROL_STEP_ANY = {'class': 'form-control', 'step': 'any'}

BOOLEAN_FIELD = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs=FORM_CHECK_INPUT_ATTRS)
    )
CHAR_FIELD = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs=FORM_CONTROL_ATTRS)
    )
FLOAT_FIELD = forms.FloatField(
        widget=forms.NumberInput(attrs=FORM_CONTROL_STEP_ANY)
    )
FLOAT_FIELD_OPTIONAL = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs=FORM_CONTROL_STEP_ANY)
    )


def multiple_choice_field(model):
    return forms.ModelMultipleChoiceField(
        queryset=model.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
def choice_field(choices):
    return forms.ChoiceField(
        choices=choices, 
        widget=forms.Select(FORM_CONTROL_ATTRS)
    )
def select2_field(model):
    return forms.ModelChoiceField(
        queryset=model.objects.all(), 
        widget=forms.Select(attrs=FORM_CONTROL_ATTRS)
    )

class BaseUnitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseUnitForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            unit = self.instance.units(field_name)
            if unit:
                self.fields[field_name].help_text = unit

class LayerStructureForm(forms.ModelForm):
    name = CHAR_FIELD
    released_for_coldforming = BOOLEAN_FIELD
    released_for_thermoforming = BOOLEAN_FIELD
    released_for_thermoforming_lid = BOOLEAN_FIELD
    class Meta:
        model = LayerStructure
        fields = ['name','released_for_coldforming', 'released_for_thermoforming','released_for_thermoforming_lid']

class BaseMaterialForm(BaseUnitForm,forms.ModelForm):
    thickness = FLOAT_FIELD
    class Meta:
        model = Material
        fields = ['thickness']

class MaterialForm(BaseMaterialForm):
    name = CHAR_FIELD
    class Meta(BaseMaterialForm.Meta):
        fields = ['name'] + BaseMaterialForm.Meta.fields

class BaseColdformingStampForm(BaseUnitForm,forms.ModelForm):
    friction_coefficient = FLOAT_FIELD
    class Meta:
        model = ColdformingStamp
        fields = ['friction_coefficient']

class ColdformingStampForm(BaseColdformingStampForm):
    name = CHAR_FIELD
    class Meta(BaseColdformingStampForm.Meta):
        fields = ['name'] + BaseColdformingStampForm.Meta.fields

class BaseWVTRDataForm(BaseUnitForm, forms.ModelForm):
    temperature = FLOAT_FIELD
    RH = FLOAT_FIELD
    WVTR = FLOAT_FIELD
    diffusivity = FLOAT_FIELD_OPTIONAL
    solubility = FLOAT_FIELD_OPTIONAL
    class Meta:
        model = WVTRData
        fields = [ 'temperature', 'RH', 'WVTR', 'diffusivity', 'solubility']

class CreateWVTRDataForm(BaseWVTRDataForm):        
    material = select2_field(Material)
    class Meta(BaseWVTRDataForm.Meta):
        fields = ['material'] + BaseWVTRDataForm.Meta.fields

class UpdateWVTRDataForm(BaseWVTRDataForm):
    class Meta(BaseWVTRDataForm.Meta):
        fields = BaseWVTRDataForm.Meta.fields

class BaseOTRDataForm(BaseUnitForm, forms.ModelForm):
    temperature = FLOAT_FIELD
    RH = FLOAT_FIELD
    OTR = FLOAT_FIELD
    diffusivity = FLOAT_FIELD_OPTIONAL
    solubility = FLOAT_FIELD_OPTIONAL
    class Meta:
        model = OTRData
        fields = [ 'temperature', 'RH', 'OTR', 'diffusivity', 'solubility']

class CreateOTRDataForm(BaseOTRDataForm):
    material = select2_field(Material)
    class Meta(BaseOTRDataForm.Meta):
        fields = ['material'] + BaseOTRDataForm.Meta.fields

class UpdateOTRDataForm(BaseOTRDataForm):
    class Meta(BaseOTRDataForm.Meta):
        fields = BaseOTRDataForm.Meta.fields

class BaseDensityDataForm(BaseUnitForm,forms.ModelForm):
    density = FLOAT_FIELD
    temperature = FLOAT_FIELD
    class Meta:
        model = DensityData
        fields = ['density', 'temperature']

class CreateDensityDataForm(BaseDensityDataForm):
    material = select2_field(Material)
    class Meta(BaseDensityDataForm.Meta):
        fields = ['material'] + BaseDensityDataForm.Meta.fields

class UpdateDensityDataForm(BaseDensityDataForm):
    class Meta(BaseDensityDataForm.Meta):
        fields = BaseDensityDataForm.Meta.fields

class BaseYoungsModulusDataForm(BaseUnitForm,forms.ModelForm):
    direction = choice_field(YoungsModulusData.DIRECTION_CHOICES)
    youngs_modulus= FLOAT_FIELD
    poissons_ratio = FLOAT_FIELD
    temperature = FLOAT_FIELD
    class Meta:
        model = YoungsModulusData
        fields = ['direction', 'youngs_modulus','poissons_ratio','temperature']

class CreateYoungsModulusDataForm(BaseYoungsModulusDataForm):
    material = select2_field(Material)
    class Meta(BaseYoungsModulusDataForm.Meta):
        fields = ['material'] + BaseYoungsModulusDataForm.Meta.fields

class UpdateYoungsModulusDataForm(BaseYoungsModulusDataForm):
    class Meta(BaseYoungsModulusDataForm.Meta):
        fields = BaseYoungsModulusDataForm.Meta.fields

class ThermoformingDataForm(forms.ModelForm): 
    material = select2_field(Material)
    class Meta:
        model = ThermoformingData
        fields = [
            'material', 
        ]
class ThermoformingDataUpdateForm(forms.ModelForm):
    wvtr_data = multiple_choice_field(WVTRData)
    otr_data = multiple_choice_field(OTRData)
    density_data = multiple_choice_field(DensityData)
    youngs_modulus_data = multiple_choice_field(YoungsModulusData)
    tensile_curve_data = multiple_choice_field(TensileCurveData)
    def __init__(self, *args, **kwargs):
        super(ThermoformingDataUpdateForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.material:
            self.fields['wvtr_data'].queryset = WVTRData.objects.filter(material=self.instance.material)
            self.fields['otr_data'].queryset = OTRData.objects.filter(material=self.instance.material)
            self.fields['density_data'].queryset = DensityData.objects.filter(material=self.instance.material)
            self.fields['youngs_modulus_data'].queryset = YoungsModulusData.objects.filter(material=self.instance.material)
            self.fields['tensile_curve_data'].queryset = TensileCurveData.objects.filter(material=self.instance.material)
        else:
            self.fields['wvtr_data'].queryset = WVTRData.objects.none()
            self.fields['otr_data'].queryset = OTRData.objects.none()
            self.fields['density_data'].queryset = DensityData.objects.none()
            self.fields['youngs_modulus_data'].queryset = YoungsModulusData.objects.none()
            self.fields['tensile_curve_data'].queryset = TensileCurveData.objects.none()
    class Meta:
        model = ThermoformingData
        fields = [
            'wvtr_data',
            'otr_data',
            'density_data',
            'youngs_modulus_data',
            'tensile_curve_data'
        ]
class ColdformingDataForm(forms.ModelForm): 
    material = select2_field(Material)
    class Meta:
        model = ColdformingData
        fields = [
            'material', 
        ]

class ColdformingDataUpdateForm(forms.ModelForm):
    youngs_modulus_data = multiple_choice_field(YoungsModulusData)
    tensile_curve_data = multiple_choice_field(TensileCurveData)
    drucker_prager_curve_data = multiple_choice_field(DruckerPragerCurveData)
    def __init__(self, *args, **kwargs):
        super(ColdformingDataUpdateForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.material:
            self.fields['youngs_modulus_data'].queryset = YoungsModulusData.objects.filter(material=self.instance.material)
            self.fields['tensile_curve_data'].queryset = TensileCurveData.objects.filter(material=self.instance.material)
            self.fields['drucker_prager_curve_data'].queryset = DruckerPragerCurveData.objects.filter(material=self.instance.material)
        else:
            self.fields['youngs_modulus_data'].queryset = YoungsModulusData.objects.none()
            self.fields['tensile_curve_data'].queryset = TensileCurveData.objects.none()
            self.fields['drucker_prager_curve_data'].queryset = DruckerPragerCurveData.objects.none()
    class Meta:
        model = ColdformingData
        fields = [
            'youngs_modulus_data',
            'tensile_curve_data',
            'drucker_prager_curve_data'
        ]

class ThermoformingLidDataForm(forms.ModelForm): 
    material = select2_field(Material)
    class Meta:
        model = ThermoformingLidData
        fields = [
            'material', 
        ]

class ThermoformingLidDataUpdateForm(forms.ModelForm):
    wvtr_data = multiple_choice_field(WVTRData)
    otr_data = multiple_choice_field(OTRData)

    def __init__(self, *args, **kwargs):
        super(ThermoformingLidDataUpdateForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.material:
            self.fields['wvtr_data'].queryset = WVTRData.objects.filter(material=self.instance.material)
            self.fields['otr_data'].queryset = OTRData.objects.filter(material=self.instance.material)
        else:
            self.fields['wvtr_data'].queryset = WVTRData.objects.none()
            self.fields['otr_data'].queryset = OTRData.objects.none()

    class Meta:
        model = ThermoformingLidData
        fields = [
            'wvtr_data',
            'otr_data',
        ]

class BaseTensileCurveDataForm(BaseUnitForm,forms.ModelForm):
    strain_rate = FLOAT_FIELD
    temperature = FLOAT_FIELD
    direction = choice_field(TensileCurveData.DIRECTION_CHOICES)
    class Meta: 
        model = TensileCurveData
        fields = ['strain_rate', 'temperature', 'direction']

class CreateTensileCurveDataForm(BaseTensileCurveDataForm):
    material = select2_field(Material)
    class Meta(BaseTensileCurveDataForm.Meta):
        fields = ['material'] + BaseTensileCurveDataForm.Meta.fields

class UpdateTensileCurveDataForm(BaseTensileCurveDataForm):
    class Meta(BaseTensileCurveDataForm.Meta):
        fields = BaseTensileCurveDataForm.Meta.fields

class BaseDruckerPragerCurveDataForm(BaseUnitForm,forms.ModelForm):
    input1 = FLOAT_FIELD
    input2 = FLOAT_FIELD
    input3 = FLOAT_FIELD
    direction = choice_field(DruckerPragerCurveData.DIRECTION_CHOICES)
    class Meta: 
        model = DruckerPragerCurveData
        fields = ['input1', 'input2', 'input3', 'direction']

class CreateDruckerPragerCurveDataForm(BaseDruckerPragerCurveDataForm):
    material = select2_field(Material)
    class Meta(BaseDruckerPragerCurveDataForm.Meta):
        fields = ['material'] + BaseDruckerPragerCurveDataForm.Meta.fields

class UpdateDruckerPragerCurveDataForm(BaseDruckerPragerCurveDataForm):
    class Meta(BaseDruckerPragerCurveDataForm.Meta):
        fields = BaseDruckerPragerCurveDataForm.Meta.fields