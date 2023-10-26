from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
import json
from django.http import HttpResponse
from ..models import LayerStructure, MaterialOrder, Material, WVTRData, ThermoformingData, DensityData, YoungsModulusData,  TensileCurveData, TensileCurvePoint
from ..forms import CreateLayerStructureForm, CreateMaterialForm, UpdateMaterialForm, CreateWVTRDataForm, UpdateWVTRDataForm, ThermoformingDataForm, CreateDensityDataForm, UpdateDensityDataForm, CreateYoungsModulusDataForm, UpdateYoungsModulusDataForm, CreateTensileCurveDataForm, UpdateTensileCurveDataForm,  ThermoformingDataUpdateForm
from django.forms import inlineformset_factory
from django import forms

class LayerStructureCreateView(CreateView):
    model = LayerStructure
    form_class = CreateLayerStructureForm
    template_name = 'form_templates/createlayerstructure.html'
    success_url = reverse_lazy('layer_structure_list')
    extra_context = {'form_title': 'Create Layer Structure'}

    def form_valid(self, form): 
        print("form_valid()")
        form.instance.name = self.request.POST.get('name')
        response = super().form_valid(form)
        ordered_material_ids = self.request.POST.get('ordered_material_ids', '').split(',')
        for order, material_id in enumerate(ordered_material_ids):
            material = Material.objects.get(id=material_id)
            MaterialOrder.objects.create(material=material, layer_structure=self.object, order=order)
        return response
    
    def form_invalid(self, form):
        print(self.request.POST)
        print("form_invalid()")
        print("Form errors:", form.errors)
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        materials = Material.objects.all().values('id', 'name')
        context['all_materials_json'] = json.dumps(list(materials))
        print(context['all_materials_json'] )
        return context

class MaterialCreateView(CreateView):
    model = Material
    form_class = CreateMaterialForm
    template_name = 'form_templates/form_template.html' 
    success_url = reverse_lazy('material_list')
    extra_context = {'form_title': 'Create Material'}
    

class MaterialUpdateView(UpdateView):
    model = Material
    form_class = UpdateMaterialForm
    template_name = 'form_templates/form_template.html'
    success_url = reverse_lazy('material_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Material'
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
        TensileCurvePointFormSet = inlineformset_factory(
           TensileCurveData,
           TensileCurvePoint,
            fields=('stress', 'strain'),
            widgets={
                'stress': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
                'strain': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
            },
            extra=0,
            can_delete=True
        )  
        # Save the main object
        self.object.save()

        # Handling the formset
        print(self.request.POST)
        formset = TensileCurvePointFormSet(self.request.POST, instance=self.object)
        
        if formset.is_valid():
            formset.save()
        else:
            print("Formset is not valid")
            print(formset.errors)

            return HttpResponse("Error: Formset is not valid.")
        return response

class TensileCurveDataCreateView(TensileCurveDataFormMixin, CreateView):
    model = TensileCurveData
    form_class = CreateTensileCurveDataForm

    template_name = 'form_templates/form_template.html'
    extra_context = {'form_title': 'Create Tensile Curve Data'}

    def get_context_data(self, **kwargs):
        TensileCurvePointFormSet = inlineformset_factory(
            TensileCurveData,
            TensileCurvePoint,
            fields=('stress', 'strain'),
            widgets={
                'stress': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
                'strain': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
            },
            extra=3,
            can_delete=True
        ) 
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = TensileCurvePointFormSet(self.request.POST)
        else:
            context['formset'] = TensileCurvePointFormSet()
     
        context['formset_name'] = 'tensilecurvepoint_set'
        context['formset_fields'] = [
            {
                'field':'stress',
                'label':'Stress',
                'type':'number',
                'required': "true",
                'step':'any'
             }, 
            {
                'field':'strain',
                'label':'Strain',
                'type':'number',
                'required': "true",
                'step':'any'
            }
            ]
        # Generate initial data for the formset dynamically
        initial_data = []
        for form in context['formset']:
            # model_to_dict takes a model instance and returns a dictionary with model's field values
            form_initial = model_to_dict(form.instance)
            initial_data.append(form_initial)
        context['formset_initial'] = json.dumps(initial_data)
        context['upload_excel_flag'] = True
        return context

class TensileCurveDataUpdateView(TensileCurveDataFormMixin, UpdateView):
    model = TensileCurveData
    form_class = UpdateTensileCurveDataForm
    template_name = 'form_templates/form_template.html'
    def get_context_data(self, **kwargs):
        TensileCurvePointFormSet = inlineformset_factory(
            TensileCurveData,
            TensileCurvePoint,
            fields=('stress', 'strain'),
            widgets={
                'stress': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
                'strain': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'})
            },
            extra=0,
            can_delete=True
        )  
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Tensile Curve Data'
        if self.request.POST:
            context['formset'] = TensileCurvePointFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = TensileCurvePointFormSet(instance=self.object)
        context['formset_name'] = 'tensilecurvepoint_set'
        context['formset_fields'] = [
            {
                'field':'stress',
                'label':'Stress',
                'type':'number',
                'required': "true",
                'step':'any'
             }, 
            {
                'field':'strain',
                'label':'Strain',
                'type':'number',
                'required': "true",
                'step':'any'
            }
            ]
        # Generate initial data for the formset dynamically
        initial_data = []
        for form in context['formset']:
            # model_to_dict takes a model instance and returns a dictionary with model's field values
            form_initial = model_to_dict(form.instance)
            form_initial["is_deleted"] = False
            initial_data.append(form_initial)


        context['formset_initial'] = json.dumps(initial_data)
        print(context['formset_initial'])
        context['display_context'] = {
            "material": self.object.material,
            "tensile id": self.object.id
        }
        return context
    

class ThermoformingDataCreateView(CreateView):
    model = ThermoformingData
    form_class = ThermoformingDataForm
    template_name = 'form_templates/form_template.html' 
    success_url = reverse_lazy('thermoformingdata_list')
    extra_context = {'form_title': 'Create Thermoforming Material'}

class ThermoformingDataUpdateView(UpdateView):
    model = ThermoformingData
    form_class = ThermoformingDataUpdateForm
    template_name = 'form_templates/form_template.html'
    success_url = reverse_lazy('thermoformingdata_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Call custom save to perform validations
        self.object.save()

        # Update many-to-many fields
        self.object.wvtr_data.set(form.cleaned_data['wvtr_data'])
        self.object.density_data.set(form.cleaned_data['density_data'])
        self.object.youngs_modulus_data.set(form.cleaned_data['youngs_modulus_data'])
        self.object.tensile_curve_data.set(form.cleaned_data['tensile_curve_data'])
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Linked Thermoforming Data'
        context['display_context'] = {
            "material": self.object.material,
            "thermoforming id": self.object.id
        }
        return context