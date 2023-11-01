from django.views.generic import DetailView
import json
from .models import ThermoformingData, ThermoformingLidData, ColdformingData
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ThermoformingDataSerializer , ThermoformingLidDataSerializer, ColdformingDataSerializer
from django.core.exceptions import ObjectDoesNotExist

from .view_modules.list_views import ColdformingDataListView, ColdformingStampListView,ThermoformingLidDataListView, DruckerPragerCurveDataListView, LayerStructureListView, ThermoformingDataListView, MaterialListView,OTRDataListView, WVTRDataListView,TensileCurveDataListView, DensityDataListView, YoungsModulusDataListView
from .view_modules.create_update_views import ColdformingDataCreateView, ColdformingDataUpdateView, ColdformingStampCreateView, ColdformingStampUpdateView,DruckerPragerCurveDataCreateView, DruckerPragerCurveDataUpdateView, LayerStructureUpdateView, LayerStructureCreateView, MaterialCreateView, MaterialUpdateView,OTRDataCreateView, OTRDataUpdateView,  WVTRDataCreateView, WVTRDataUpdateView, DensityDataCreateView, DensityDataUpdateView, YoungsModulusDataCreateView, YoungsModulusDataUpdateView, TensileCurveDataCreateView, TensileCurveDataUpdateView, ThermoformingDataCreateView, ThermoformingDataUpdateView, ThermoformingLidDataCreateView, ThermoformingLidDataUpdateView
from .view_modules.delete_views import ColdformingDataDeleteView, ColdformingStampDeleteView, DruckerPragerCurveDataDeleteView, LayerStructureDeleteView, MaterialDeleteView,OTRDataDeleteView, WVTRDataDeleteView, DensityDataDeleteView, YoungsModulusDataDeleteView, TensileCurveDataDeleteView, ThermoformingDataDeleteView, ThermoformingLidDataDeleteView
from django.shortcuts import render

def guide(request):
    return render(request, 'guide.html')

class ThermoformingDataAPI(APIView):
    def get(self, request, thermoforming_id, format=None):
        try:
            thermoforming_data = ThermoformingData.objects.get(pk=thermoforming_id)
            serializer = ThermoformingDataSerializer(thermoforming_data)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({})

class ColdformingDataAPI(APIView):
    def get(self, request, coldforming_id, format=None):
        try:
            coldforming_data = ColdformingData.objects.get(pk=coldforming_id)
            serializer = ColdformingDataSerializer(coldforming_data)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({})

class ThermoformingLidDataAPI(APIView):
    def get(self, request, thermoforming_lid_id, format=None):
        try:
            thermoforming_lid_data = ThermoformingLidData.objects.get(pk=thermoforming_lid_id)
            serializer = ThermoformingLidDataSerializer(thermoforming_lid_data)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({})
    
    
class ThermoformingDataDetailView(DetailView):
    model = ThermoformingData
    template_name = 'thermoformingdata_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wvtr_data'] = self.object.get_associated_wvtr_data()
        context['otr_data'] = self.object.get_associated_otr_data()
        context['density_data'] = self.object.get_associated_density_data()
        context['youngs_modulus_data'] = self.object.get_associated_youngs_modulus_data()

        context['tensile_data'] = self.object.get_associated_tensile_data()
        context['tensile_data_json'] = json.dumps(self.object.get_associated_tensile_data())
        return context

class ColdformingDataDetailView(DetailView):
    model = ColdformingData
    template_name = 'coldformingdata_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['youngs_modulus_data'] = self.object.get_associated_youngs_modulus_data()
        context['tensile_data'] = self.object.get_associated_tensile_data()
        context['tensile_data_json'] = json.dumps(self.object.get_associated_tensile_data())
        context['drucker_prager_data'] = self.object.get_associated_drucker_prager_data()
        context['drucker_prager_data_json'] = json.dumps(self.object.get_associated_drucker_prager_data())
        return context

class ThermoformingLidDataDetailView(DetailView):
    model = ThermoformingLidData
    template_name = 'thermoformingliddata_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wvtr_data'] = self.object.get_associated_wvtr_data()
        context['otr_data'] = self.object.get_associated_otr_data()
        return context