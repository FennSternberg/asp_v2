from django import forms
from .models import  ColdformingStamp, LayerStructure, Material, DensityData, OTRData, WVTRData,ColdformingData, ThermoformingData, ThermoformingLidData, YoungsModulusData,  TensileCurveData, DruckerPragerCurveData


class BaseUnitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseUnitForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            unit = self.instance.units(field_name)
            if unit:
                self.fields[field_name].help_text = unit

class CreateLayerStructureForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    released_for_coldforming = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    released_for_thermoforming = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    released_for_thermoforming_lid = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = LayerStructure
        fields = ['name','released_for_coldforming', 'released_for_thermoforming','released_for_thermoforming_lid']

class BaseMaterialForm(BaseUnitForm,forms.ModelForm):
    thickness = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    class Meta:
        model = Material
        fields = ['thickness']

class CreateMaterialForm(BaseMaterialForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta(BaseMaterialForm.Meta):
        fields = ['name'] + BaseMaterialForm.Meta.fields
    
class UpdateMaterialForm( BaseMaterialForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta(BaseMaterialForm.Meta):
        fields = ['name'] + BaseMaterialForm.Meta.fields

class BaseColdformingStampForm(BaseUnitForm,forms.ModelForm):
    friction_coefficient = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    class Meta:
        model = ColdformingStamp
        fields = ['friction_coefficient']

class CreateColdformingStampForm(BaseColdformingStampForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta(BaseColdformingStampForm.Meta):
        fields = ['name'] + BaseColdformingStampForm.Meta.fields
    
class UpdateColdformingStampForm( BaseColdformingStampForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    class Meta(BaseColdformingStampForm.Meta):
        fields = ['name'] + BaseColdformingStampForm.Meta.fields

class BaseWVTRDataForm(BaseUnitForm, forms.ModelForm):

    temperature = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    RH = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    WVTR = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    diffusivity = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    solubility = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    class Meta:
        model = WVTRData
        fields = [ 'temperature', 'RH', 'WVTR', 'diffusivity', 'solubility']

class CreateWVTRDataForm(BaseWVTRDataForm):
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta(BaseWVTRDataForm.Meta):
        fields = ['material'] + BaseWVTRDataForm.Meta.fields

class UpdateWVTRDataForm(BaseWVTRDataForm):
    class Meta(BaseWVTRDataForm.Meta):
        # No 'material' field
        fields = BaseWVTRDataForm.Meta.fields


class BaseOTRDataForm(BaseUnitForm, forms.ModelForm):

    temperature = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    RH = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    OTR = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    diffusivity = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    solubility = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    class Meta:
        model = OTRData
        fields = [ 'temperature', 'RH', 'OTR', 'diffusivity', 'solubility']

class CreateOTRDataForm(BaseOTRDataForm):
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta(BaseOTRDataForm.Meta):
        fields = ['material'] + BaseOTRDataForm.Meta.fields

class UpdateOTRDataForm(BaseOTRDataForm):
    class Meta(BaseOTRDataForm.Meta):
        # No 'material' field
        fields = BaseOTRDataForm.Meta.fields

# density

class BaseDensityDataForm(BaseUnitForm,forms.ModelForm):
    density = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    temperature = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    class Meta:
        model = DensityData
        fields = ['density', 'temperature']

class CreateDensityDataForm(BaseDensityDataForm):
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta(BaseDensityDataForm.Meta):
        fields = ['material'] + BaseDensityDataForm.Meta.fields

class UpdateDensityDataForm(BaseDensityDataForm):
    class Meta(BaseDensityDataForm.Meta):
        fields = BaseDensityDataForm.Meta.fields

# YM
class BaseYoungsModulusDataForm(BaseUnitForm,forms.ModelForm):
    direction = forms.ChoiceField(
        choices=YoungsModulusData.DIRECTION_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    youngs_modulus= forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    poissons_ratio = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    temperature = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    class Meta:
        model = YoungsModulusData
        fields = ['direction', 'youngs_modulus','poissons_ratio','temperature']

class CreateYoungsModulusDataForm(BaseYoungsModulusDataForm):
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta(BaseYoungsModulusDataForm.Meta):
        fields = ['material'] + BaseYoungsModulusDataForm.Meta.fields

class UpdateYoungsModulusDataForm(BaseYoungsModulusDataForm):
    class Meta(BaseYoungsModulusDataForm.Meta):
        fields = BaseYoungsModulusDataForm.Meta.fields

class ThermoformingDataForm(forms.ModelForm): 
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = ThermoformingData
        fields = [
            'material', 
        ]
class ThermoformingDataUpdateForm(forms.ModelForm):
    wvtr_data = forms.ModelMultipleChoiceField(
        queryset=WVTRData.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    otr_data = forms.ModelMultipleChoiceField(
        queryset=OTRData.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    density_data = forms.ModelMultipleChoiceField(
        queryset=DensityData.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    youngs_modulus_data = forms.ModelMultipleChoiceField(
        queryset=YoungsModulusData.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    tensile_curve_data = forms.ModelMultipleChoiceField(
        queryset=TensileCurveData.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
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
# coldforming

class ColdformingDataForm(forms.ModelForm): 
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = ColdformingData
        fields = [
            'material', 
        ]

class ColdformingDataUpdateForm(forms.ModelForm):
    youngs_modulus_data = forms.ModelMultipleChoiceField(
        queryset=YoungsModulusData.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    tensile_curve_data = forms.ModelMultipleChoiceField(
        queryset=TensileCurveData.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    drucker_prager_curve_data = forms.ModelMultipleChoiceField(
        queryset=DruckerPragerCurveData.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
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
# lid

class ThermoformingLidDataForm(forms.ModelForm): 
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = ThermoformingLidData
        fields = [
            'material', 
        ]
class ThermoformingLidDataUpdateForm(forms.ModelForm):
    wvtr_data = forms.ModelMultipleChoiceField(
        queryset=WVTRData.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )
    otr_data = forms.ModelMultipleChoiceField(
        queryset=OTRData.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

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
# Stress Strain

class BaseTensileCurveDataForm(BaseUnitForm,forms.ModelForm):
    strain_rate = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    temperature = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    direction = forms.ChoiceField(
        choices=TensileCurveData.DIRECTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta: 
        model = TensileCurveData
        fields = ['strain_rate', 'temperature', 'direction']

class CreateTensileCurveDataForm(BaseTensileCurveDataForm):
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta(BaseTensileCurveDataForm.Meta):
        fields = ['material'] + BaseTensileCurveDataForm.Meta.fields

class UpdateTensileCurveDataForm(BaseTensileCurveDataForm):
    class Meta(BaseTensileCurveDataForm.Meta):
        fields = BaseTensileCurveDataForm.Meta.fields



class BaseDruckerPragerCurveDataForm(BaseUnitForm,forms.ModelForm):
    input1 = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    input2 = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    input3 = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
    )
    direction = forms.ChoiceField(
        choices=DruckerPragerCurveData.DIRECTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta: 
        model = DruckerPragerCurveData
        fields = ['input1', 'input2', 'input3', 'direction']

class CreateDruckerPragerCurveDataForm(BaseDruckerPragerCurveDataForm):
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(), 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta(BaseDruckerPragerCurveDataForm.Meta):
        fields = ['material'] + BaseDruckerPragerCurveDataForm.Meta.fields

class UpdateDruckerPragerCurveDataForm(BaseDruckerPragerCurveDataForm):
    class Meta(BaseDruckerPragerCurveDataForm.Meta):
        fields = BaseDruckerPragerCurveDataForm.Meta.fields