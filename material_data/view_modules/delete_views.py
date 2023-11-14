from django.views.generic import DeleteView
from django.urls import reverse_lazy
from ..models import ThermoformingPlug, ColdformingStamp, Material, WVTRData, OTRData,ColdformingData, ThermoformingData, ThermoformingLidData, DensityData, YoungsModulusData,  TensileCurveData, DruckerPragerCurveData, LayerStructure

class DeleteViewMixin:
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy(f"{self.model.__name__.lower()}_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.model.__name__.replace("Data", " Data")
        context['delete_title'] = f'Delete {model_name}'
        context['delete_message'] = f'Are you sure you want to delete this {model_name.lower()}?'
        context['cancel_url'] = self.get_success_url()
        return context

class MaterialDeleteView(DeleteViewMixin, DeleteView):
    model = Material

class ColdformingStampDeleteView(DeleteViewMixin, DeleteView):
    model = ColdformingStamp

class ThermoformingPlugDeleteView(DeleteViewMixin, DeleteView):
    model = ThermoformingPlug

class WVTRDataDeleteView(DeleteViewMixin, DeleteView):
    model = WVTRData

class OTRDataDeleteView(DeleteViewMixin, DeleteView):
    model = OTRData
    
class DensityDataDeleteView(DeleteViewMixin, DeleteView):
    model = DensityData

class YoungsModulusDataDeleteView(DeleteViewMixin, DeleteView):
    model = YoungsModulusData

class TensileCurveDataDeleteView(DeleteViewMixin, DeleteView):
    model = TensileCurveData

class DruckerPragerCurveDataDeleteView(DeleteViewMixin, DeleteView):
    model = DruckerPragerCurveData

class ThermoformingDataDeleteView(DeleteViewMixin, DeleteView):
    model = ThermoformingData

class ColdformingDataDeleteView(DeleteViewMixin, DeleteView):
    model = ColdformingData

class ThermoformingLidDataDeleteView(DeleteViewMixin, DeleteView):
    model = ThermoformingLidData

class LayerStructureDeleteView(DeleteViewMixin, DeleteView):
    model = LayerStructure
