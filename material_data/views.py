from django.views.generic import DetailView
import json
from .models import ThermoformingData
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ThermoformingDataSerializer 
from django.core.exceptions import ObjectDoesNotExist

from .view_modules.list_views import  LayerStructureListView, ThermoformingDataListView, MaterialListView,WVTRDataListView,TensileCurveDataListView, DensityDataListView, YoungsModulusDataListView
from .view_modules.create_update_views import LayerStructureCreateView, MaterialCreateView, MaterialUpdateView, WVTRDataCreateView, WVTRDataUpdateView, DensityDataCreateView, DensityDataUpdateView, YoungsModulusDataCreateView, YoungsModulusDataUpdateView, TensileCurveDataCreateView, TensileCurveDataUpdateView, ThermoformingDataCreateView, ThermoformingDataUpdateView
from .view_modules.delete_views import LayerStructureDeleteView, MaterialDeleteView, WVTRDataDeleteView, DensityDataDeleteView, YoungsModulusDataDeleteView, TensileCurveDataDeleteView, ThermoformingDataDeleteView

class ThermoformingDataAPI(APIView):
    def get(self, request, thermoforming_id, format=None):
        try:
            thermoforming_data = ThermoformingData.objects.get(pk=thermoforming_id)
            serializer = ThermoformingDataSerializer(thermoforming_data)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({})
    
    
class ThermoformingDataDetailView(DetailView):
    model = ThermoformingData
    template_name = 'thermoformingdata_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wvtr_data'] = self.object.get_associated_wvtr_data()
        context['density_data'] = self.object.get_associated_density_data()
        context['youngs_modulus_data'] = self.object.get_associated_youngs_modulus_data()

        context['tensile_data'] = self.object.get_associated_tensile_data()
        context['tensile_data_json'] = json.dumps(self.object.get_associated_tensile_data())
        return context 