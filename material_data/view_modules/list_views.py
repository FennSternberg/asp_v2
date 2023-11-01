from django.views.generic import ListView
from ..models import LayerStructure,ColdformingStamp, MaterialOrder, Material,OTRData, WVTRData,ColdformingData, ThermoformingData,ThermoformingLidData, DensityData, YoungsModulusData,  TensileCurveData, TensileCurvePoint, DruckerPragerCurveData, DruckerPragerCurvePoint
from django.db.models import Q
from django.db.models import Prefetch

class FieldUnitsMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create a dictionary to hold field-units mapping
        field_units = {}
        if context['object_list']:
            first_object = context['object_list'][0]
            for field in self.model._meta.get_fields():
                field_name = field.name
                unit = first_object.units(field_name)
                if unit:
                    field_units[field_name] = unit  # Removed the "_unit" suffix for consistency
        context['field_units'] = field_units
        print(field_units)
        return context

class SearchMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search')

        if query:
            queryset = queryset.filter(
                Q(material__name__icontains=query)
            ).distinct()
        return queryset

class LayerStructureListView(ListView):
    model = LayerStructure
    template_name = 'list_templates/layerstructure_list.html'
    def get_queryset(self):
        query = self.request.GET.get('search')
        queryset = super().get_queryset()

        if query:
            layer_structure_ids_with_material = MaterialOrder.objects.filter(
                material__name__icontains=query
            ).values_list('layer_structure_id', flat=True).distinct()
            queryset = queryset.filter( Q(id__in=layer_structure_ids_with_material) | Q(name__icontains=query))

        materials_ordered = MaterialOrder.objects.filter(
            layer_structure__in=queryset
        ).order_by('order')
        print( materials_ordered) 
        queryset = queryset.prefetch_related(
            Prefetch('materialorder_set', queryset=materials_ordered, to_attr='ordered_materials')
        )
        print(queryset)
        
        return queryset

class ThermoformingDataListView(SearchMixin, ListView):
    model = ThermoformingData
    template_name = 'list_templates/thermoformingdata_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related(
            'wvtr_data',
            'otr_data',
            'density_data',
            'youngs_modulus_data',
            'tensile_curve_data',
        )

        for data in queryset:
            data.wvtr_count = data.wvtr_data.count()
            data.otr_count = data.otr_data.count()
            data.density_count = data.density_data.count()
            data.YM_CD_count = data.youngs_modulus_data.filter(direction='CD').count()
            data.YM_MD_count = data.youngs_modulus_data.filter(direction='MD').count()
            data.tensile_CD_count = data.tensile_curve_data.filter(direction='CD').count()
            data.tensile_MD_count = data.tensile_curve_data.filter(direction='MD').count()
        return queryset

class ColdformingDataListView(SearchMixin, ListView):
    model = ColdformingData
    template_name = 'list_templates/coldformingdata_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related(
            'youngs_modulus_data',
            'tensile_curve_data',
            'drucker_prager_curve_data'
        )

        for data in queryset:
            data.YM_CD_count = data.youngs_modulus_data.filter(direction='CD').count()
            data.YM_MD_count = data.youngs_modulus_data.filter(direction='MD').count()
            data.tensile_CD_count = data.tensile_curve_data.filter(direction='CD').count()
            data.tensile_MD_count = data.tensile_curve_data.filter(direction='MD').count()
            data.drucker_prager_CD_count = data.drucker_prager_curve_data.filter(direction='CD').count()
            data.drucker_prager_MD_count = data.drucker_prager_curve_data.filter(direction='MD').count()
        return queryset

class ThermoformingLidDataListView(SearchMixin, ListView):
    model = ThermoformingLidData
    template_name = 'list_templates/thermoformingliddata_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related(
            'wvtr_data',
            'otr_data',
        )
        for data in queryset:
            data.wvtr_count = data.wvtr_data.count()
            data.otr_count = data.otr_data.count()
        return queryset
    
class MaterialListView(FieldUnitsMixin,ListView):
    model = Material
    template_name = 'list_templates/material_list.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) 
            ).distinct()

        return queryset
class ColdformingStampListView(FieldUnitsMixin,ListView):
    model = ColdformingStamp
    template_name = 'list_templates/coldformingstamp_list.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) 
            ).distinct()
        return queryset
    
class WVTRDataListView(FieldUnitsMixin, SearchMixin, ListView):
    model = WVTRData
    template_name = 'list_templates/wvtrdata_list.html'

class OTRDataListView(FieldUnitsMixin, SearchMixin, ListView):
    model = OTRData
    template_name = 'list_templates/otrdata_list.html'
 
    
class TensileCurveDataListView(FieldUnitsMixin, SearchMixin,ListView):
    model = TensileCurveData
    template_name = 'list_templates/tensilecurvedata_list.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        for data in queryset:
            data.point_count = TensileCurvePoint.objects.filter(tensile_curve_id=data.id).count()
        return queryset
    
class DruckerPragerCurveDataListView(FieldUnitsMixin, SearchMixin,ListView):
    model = DruckerPragerCurveData
    template_name = 'list_templates/druckerpragercurvedata_list.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        for data in queryset:
            data.point_count = DruckerPragerCurvePoint.objects.filter(drucker_prager_curve_id=data.id).count()
        return queryset

class DensityDataListView(FieldUnitsMixin, SearchMixin,ListView):
    model = DensityData
    template_name = 'list_templates/densitydata_list.html'
    
class YoungsModulusDataListView(FieldUnitsMixin, SearchMixin, ListView):
    model = YoungsModulusData
    template_name = 'list_templates/youngsmodulusdata_list.html'