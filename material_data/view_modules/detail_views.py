from django.views.generic import DetailView
import json
from ..models import ThermoformingData, ThermoformingLidData, ColdformingData

class ThermoformingDataDetailView(DetailView):
    model = ThermoformingData
    template_name = 'detail_templates/thermoformingdata_detail.html'
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
    template_name = 'detail_templates/coldformingdata_detail.html'
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
    template_name = 'detail_templates/thermoformingliddata_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wvtr_data'] = self.object.get_associated_wvtr_data()
        context['otr_data'] = self.object.get_associated_otr_data()
        return context