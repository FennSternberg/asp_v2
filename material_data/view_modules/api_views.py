from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from ..models import ThermoformingData, ThermoformingLidData, ColdformingData
from ..serializers import ThermoformingDataSerializer , ThermoformingLidDataSerializer, ColdformingDataSerializer

# Base API class with common functionality
class BaseDataAPI(APIView):
    model = None  # Override in subclass
    serializer_class = None  # Override in subclass

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    def get(self, request, pk, format=None):
        obj = self.get_object(pk)
        if obj is not None:
            serializer = self.serializer_class(obj)
            return Response(serializer.data)
        return Response({})

# Subclasses for specific data types
class ThermoformingDataAPI(BaseDataAPI):
    model = ThermoformingData
    serializer_class = ThermoformingDataSerializer

class ColdformingDataAPI(BaseDataAPI):
    model = ColdformingData
    serializer_class = ColdformingDataSerializer

class ThermoformingLidDataAPI(BaseDataAPI):
    model = ThermoformingLidData
    serializer_class = ThermoformingLidDataSerializer
