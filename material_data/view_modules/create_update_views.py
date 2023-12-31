from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
import json
from django.http import HttpResponse
from ..models import LayerStructure, ThermoformingPlug, ColdformingStamp, MaterialOrder, Material, OTRData, WVTRData, ColdformingData, ThermoformingLidData, ThermoformingData, DensityData, YoungsModulusData, DruckerPragerCurveData, DruckerPragerCurvePoint,  TensileCurveData, TensileCurvePoint
from ..forms import ThermoformingPlugForm, ColdformingStampForm, LayerStructureForm, MaterialForm, CreateOTRDataForm, UpdateOTRDataForm, CreateWVTRDataForm, UpdateWVTRDataForm, ThermoformingDataForm,ThermoformingLidDataForm, ColdformingDataForm, CreateDensityDataForm, UpdateDensityDataForm, CreateYoungsModulusDataForm, UpdateYoungsModulusDataForm,CreateDruckerPragerCurveDataForm, UpdateDruckerPragerCurveDataForm, CreateTensileCurveDataForm, UpdateTensileCurveDataForm,  ThermoformingDataUpdateForm, ThermoformingLidDataUpdateForm, ColdformingDataUpdateForm
from django.forms import inlineformset_factory
from django import forms


class MaterialCreateView(CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'form_templates/form_template.html' 
    success_url = reverse_lazy('material_list')
    extra_context = {'form_title': 'Create Material'}
    

class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'form_templates/form_template.html'
    success_url = reverse_lazy('material_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Material'
        context['display_context'] = {"material": self.object.name, "material id": self.object.id}
        return context

class ColdformingStampCreateView(CreateView):
    model = ColdformingStamp
    form_class = ColdformingStampForm
    template_name = 'form_templates/form_template.html' 
    success_url = reverse_lazy('coldformingstamp_list')
    extra_context = {'form_title': 'Create Coldforming Stamp'}
    

class ColdformingStampUpdateView(UpdateView):
    model = ColdformingStamp
    form_class = ColdformingStampForm
    template_name = 'form_templates/form_template.html'
    success_url = reverse_lazy('coldformingstamp_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Coldforming Stamp'
        context['display_context'] = {"material": self.object.name, "material id": self.object.id}
        return context

class ThermoformingPlugCreateView(CreateView):
    model = ThermoformingPlug
    form_class = ThermoformingPlugForm
    template_name = 'form_templates/form_template.html' 
    success_url = reverse_lazy('thermoformingplug_list')
    extra_context = {'form_title': 'Create Thermoforming Plug'}
    

class ThermoformingPlugUpdateView(UpdateView):
    model = ThermoformingPlug
    form_class = ThermoformingPlugForm
    template_name = 'form_templates/form_template.html'
    success_url = reverse_lazy('thermoformingplug_list')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Thermoforming Plug'
        context['display_context'] = {"material": self.object.name, "material id": self.object.id}
        return context

class WVTRDataFormMixin:
    success_url = reverse_lazy('wvtrdata_list')

class WVTRDataCreateView(WVTRDataFormMixin, CreateView):
    model = WVTRData
    form_class = CreateWVTRDataForm
    template_name = 'form_templates/form_template.html'
    extra_context = {'form_title': 'Create WVTR Data'}

class WVTRDataUpdateView(WVTRDataFormMixin, UpdateView):
    model = WVTRData
    form_class = UpdateWVTRDataForm
    template_name = 'form_templates/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update WVTR Data'
        context['display_context'] = {
            "material": self.object.material,
            "wvtr id": self.object.id
        }
        return context

class OTRDataFormMixin:
    success_url = reverse_lazy('otrdata_list')

class OTRDataCreateView(OTRDataFormMixin, CreateView):
    model = OTRData
    form_class = CreateOTRDataForm
    template_name = 'form_templates/form_template.html'
    extra_context = {'form_title': 'Create OTR Data'}

class OTRDataUpdateView(OTRDataFormMixin, UpdateView):
    model = OTRData
    form_class = UpdateOTRDataForm
    template_name = 'form_templates/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update OTR Data'
        context['display_context'] = {
            "material": self.object.material,
            "otr id": self.object.id
        }
        return context

class DensityDataFormMixin:
    success_url = reverse_lazy('densitydata_list')
    
class DensityDataCreateView(DensityDataFormMixin, CreateView):
    model = DensityData
    form_class = CreateDensityDataForm
    template_name = 'form_templates/form_template.html'
    extra_context = {'form_title': 'Create Density Data'}

class DensityDataUpdateView(DensityDataFormMixin, UpdateView):
    model = DensityData
    form_class = UpdateDensityDataForm
    template_name = 'form_templates/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Density Data'
        context['display_context'] = {
            "material": self.object.material,
            "density id": self.object.id
        }
        return context
    
class YoungsModulusDataFormMixin:
    success_url = reverse_lazy('youngsmodulusdata_list')
    
class YoungsModulusDataCreateView(YoungsModulusDataFormMixin, CreateView):
    model = YoungsModulusData
    form_class = CreateYoungsModulusDataForm
    template_name = 'form_templates/form_template.html'
    extra_context = {'form_title': 'Create Youngs Modulus Data'}

class YoungsModulusDataUpdateView(YoungsModulusDataFormMixin, UpdateView):
    model = YoungsModulusData
    form_class = UpdateYoungsModulusDataForm
    template_name = 'form_templates/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Youngs Modulus Data'
        context['display_context'] = {
            "material": self.object.material,
            "youngs modulus id": self.object.id
        }
        return context

class TensileCurveDataFormMixin:
    success_url = reverse_lazy('tensilecurvedata_list')

    def form_valid(self, form):
        # Capture the response from the parent class's form_valid method
        response = super().form_valid(form)
        TensileCurvePointFormSet = self.get_formset() 
        self.object.save()
        formset = TensileCurvePointFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()
        else: 
            print("Formset is not valid")
            print(formset.errors)
            return HttpResponse("Error: Formset is not valid.")
        return response
    
    def get_formset(self, extra=0):
        return inlineformset_factory(
            TensileCurveData,
            TensileCurvePoint,
            fields=('stress', 'strain'),
            widgets={
                'stress': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
                'strain': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
            },
            extra=extra,
            can_delete=True
        )
    def get_shared_context_data(self,context):
        context['formset_name'] = 'tensilecurvepoint_set'
        context['formset_fields'] = [
            {
                'field':'stress',
                'label':'Stress',
                'type':'number',
                'required': "true",
                'step':'any',
                'unit':TensileCurvePoint().units('stress')
             }, 
            {
                'field':'strain',
                'label':'Strain',
                'type':'number',
                'required': "true",
                'step':'any',
                'unit':TensileCurvePoint().units('strain')
            }
            ]
        initial_data = []
        for form in context['formset']:
            form_initial = model_to_dict(form.instance)
            form_initial["is_deleted"] = False
            initial_data.append(form_initial)
        context['formset_initial'] = json.dumps(initial_data)
        return context

class TensileCurveDataCreateView(TensileCurveDataFormMixin, CreateView):
    model = TensileCurveData
    form_class = CreateTensileCurveDataForm

    template_name = 'form_templates/form_template.html'
    extra_context = {'form_title': 'Create Tensile Curve Data'}

    def get_context_data(self, **kwargs):
        TensileCurvePointFormSet = self.get_formset(extra=3)
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = TensileCurvePointFormSet(self.request.POST)
        else:
            context['formset'] = TensileCurvePointFormSet()
        context = self.get_shared_context_data(context)
        context['upload_excel_flag'] = True
        return context

class TensileCurveDataUpdateView(TensileCurveDataFormMixin, UpdateView):
    model = TensileCurveData
    form_class = UpdateTensileCurveDataForm
    template_name = 'form_templates/form_template.html'
    def get_context_data(self, **kwargs):
        TensileCurvePointFormSet = self.get_formset() 
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Tensile Curve Data'
        if self.request.POST:
            context['formset'] = TensileCurvePointFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = TensileCurvePointFormSet(instance=self.object)
        context = self.get_shared_context_data(context)
        context['display_context'] = {
            "material": self.object.material,
            "tensile id": self.object.id
        }
        return context

class DruckerPragerCurveDataFormMixin:
    success_url = reverse_lazy('druckerpragercurvedata_list')
    def form_valid(self, form):
        response = super().form_valid(form)
        DruckerPragerCurvePointFormSet = inlineformset_factory(
           DruckerPragerCurveData,
           DruckerPragerCurvePoint,
            fields=('stress', 'strain'),
            widgets={
                'stress': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
                'strain': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
            },
            extra=0,
            can_delete=True
        )  
        self.object.save()
        formset = DruckerPragerCurvePointFormSet(self.request.POST, instance=self.object)
        
        if formset.is_valid():
            formset.save()
        else: 
            print("Formset is not valid")
            print(formset.errors)
            return HttpResponse("Error: Formset is not valid.")
        return response
    def get_formset(self,extra=0):
        return inlineformset_factory(
            DruckerPragerCurveData,
            DruckerPragerCurvePoint,
            fields=('stress', 'strain'),
            widgets={
                'stress': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
                'strain': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
            },
            extra=extra,
            can_delete=True
        )
    def get_shared_context_data(self,context):
        context['formset_name'] = 'druckerpragercurvepoint_set'
        context['formset_fields'] = [
            {
                'field':'stress',
                'label':'Stress',
                'type':'number',
                'required': 'true',
                'step':'any',
                'unit':DruckerPragerCurvePoint().units('stress')
             }, 
            {
                'field':'strain',
                'label':'Strain',
                'type':'number',
                'required': 'true',
                'step':'any',
                'unit':DruckerPragerCurvePoint().units('strain')
            }
            ]
        # Generate initial data for the formset dynamically
        initial_data = []
        for form in context['formset']:
            # model_to_dict takes a model instance and returns a dictionary with model's field values
            form_initial = model_to_dict(form.instance)
            initial_data.append(form_initial)
        context['formset_initial'] = json.dumps(initial_data)
        return context


class DruckerPragerCurveDataCreateView(DruckerPragerCurveDataFormMixin, CreateView):
    model = DruckerPragerCurveData
    form_class = CreateDruckerPragerCurveDataForm

    template_name = 'form_templates/form_template.html'
    extra_context = {'form_title': 'Create Drucker Prager Curve Data'}

    def get_context_data(self, **kwargs):
        DruckerPragerCurvePointFormSet =  self.get_formset(extra=3)
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = DruckerPragerCurvePointFormSet(self.request.POST)
        else:
            context['formset'] = DruckerPragerCurvePointFormSet()
        context = self.get_shared_context_data(context)
        context['upload_excel_flag'] = True
        return context

class DruckerPragerCurveDataUpdateView(DruckerPragerCurveDataFormMixin, UpdateView):
    model = DruckerPragerCurveData
    form_class = UpdateDruckerPragerCurveDataForm
    template_name = 'form_templates/form_template.html'
    def get_context_data(self, **kwargs):
        DruckerPragerCurvePointFormSet = self.get_formset() 
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Drucker Prager Curve Data'
        if self.request.POST:
            context['formset'] = DruckerPragerCurvePointFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = DruckerPragerCurvePointFormSet(instance=self.object)
        context = self.get_shared_context_data(context)
        context['display_context'] = {
            "material": self.object.material,
            "drucker prager id": self.object.id
        }
        return context

class ThermoformingDataCreateView(CreateView):
    model = ThermoformingData
    form_class = ThermoformingDataForm
    template_name = 'form_templates/form_template.html' 
    success_url = reverse_lazy('thermoformingdata_list')
    extra_context = {'form_title': 'Create Thermoforming Material'}

class ColdformingDataCreateView(CreateView):
    model = ColdformingData
    form_class = ColdformingDataForm
    template_name = 'form_templates/form_template.html' 
    success_url = reverse_lazy('coldformingdata_list')
    extra_context = {'form_title': 'Create Coldforming Material'}

class ThermoformingLidDataCreateView(CreateView):
    model = ThermoformingLidData
    form_class = ThermoformingLidDataForm
    template_name = 'form_templates/form_template.html' 
    success_url = reverse_lazy('thermoformingliddata_list')
    extra_context = {'form_title': 'Create Thermoforming Lid Material'}

class ApplicationDataUpdateViewMixin(UpdateView):
    template_name = 'form_templates/form_template.html'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        for field in self.many_to_many_fields:
            if field in form.cleaned_data:
                getattr(self.object, field).set(form.cleaned_data[field])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = self.form_title
        context['display_context'] = {
            "material": self.object.material,
            f"{self.data_type} id": self.object.id
        }
        return context

class ThermoformingDataUpdateView(ApplicationDataUpdateViewMixin):
    model = ThermoformingData
    form_class = ThermoformingDataUpdateForm
    success_url = reverse_lazy('thermoformingdata_list')
    many_to_many_fields = ['wvtr_data', 'otr_data', 'density_data', 'youngs_modulus_data', 'tensile_curve_data']
    form_title = 'Update Linked Thermoforming Data'
    data_type = 'thermoforming'


class ColdformingDataUpdateView(ApplicationDataUpdateViewMixin):
    model = ColdformingData
    form_class = ColdformingDataUpdateForm
    success_url = reverse_lazy('coldformingdata_list')
    many_to_many_fields = ['youngs_modulus_data', 'tensile_curve_data', 'drucker_prager_curve_data']
    form_title = 'Update Linked Coldforming Data'
    data_type = 'coldforming'


class ThermoformingLidDataUpdateView(ApplicationDataUpdateViewMixin):
    model = ThermoformingLidData
    form_class = ThermoformingLidDataUpdateForm
    success_url = reverse_lazy('thermoformingliddata_list')
    many_to_many_fields = ['wvtr_data', 'otr_data']
    form_title = 'Update Linked Thermoforming Lid Data'
    data_type = 'thermoforming lid'


class LayerStructureCreateView(CreateView):
    model = LayerStructure
    form_class = LayerStructureForm 
    template_name = 'form_templates/layerstructure_form.html'
    success_url = reverse_lazy('layerstructure_list')
    extra_context = {'form_title': 'Create Layer Structure'}

    def form_valid(self, form): 
        form.instance.name = self.request.POST.get('name')
        response = super().form_valid(form)
        ordered_material_ids = self.request.POST.get('ordered_material_ids', '').split(',')
        for order, material_id in enumerate(ordered_material_ids):
            material = Material.objects.get(id=material_id)
            MaterialOrder.objects.create(material=material, layer_structure=self.object, order=order)
        return response
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        materials = Material.objects.all().values('id', 'name')
        context['all_materials_json'] = json.dumps(list(materials))
        return context

class LayerStructureUpdateView(UpdateView):
    model = LayerStructure
    form_class = LayerStructureForm
    template_name = 'form_templates/layerstructure_form.html'
    success_url = reverse_lazy('layerstructure_list')
    extra_context = {'form_title': 'Update Layer Structure'}

    def form_valid(self, form):
        form.instance.name = self.request.POST.get('name')
        response = super().form_valid(form)
        self.object.materialorder_set.all().delete()
        ordered_material_ids = self.request.POST.get('ordered_material_ids', '').split(',')
        for order, material_id in enumerate(ordered_material_ids):
            material = Material.objects.get(id=material_id)
            MaterialOrder.objects.create(material=material, layer_structure=self.object, order=order)
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        materials = Material.objects.all().values('id', 'name')
        context['all_materials_json'] = json.dumps(list(materials))
        context['selected_materials_json'] = json.dumps(
            list(self.object.materialorder_set.all().values_list('material_id', flat=True))
        )
        return context