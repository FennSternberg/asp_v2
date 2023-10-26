from django.core.exceptions import ValidationError
from django.test import TestCase
from .models import Material, WVTRData, ThermoformingData

class PermeabilityThermoformingTest(TestCase):

    def setUp(self):
        self.material1 = Material.objects.create(name="Material 1", thickness=1.2)
        self.material2 = Material.objects.create(name="Material 2", thickness=1.3)
        self.permeability_data = WVTRData.objects.create(material=self.material1, type='wvtr', temperature=20, RH=40, transmission_rate=2.2)
        self.thermoforming_data = ThermoformingData.objects.create(material=self.material2)

    def test_association_with_different_material(self):
        # tests that a permeability test can't be associated with a different material in the thermoforming model
        self.permeability_data.thermoforming_id = self.thermoforming_data
        with self.assertRaises(ValidationError):
            self.permeability_data.save()
    
    def test_association_with_same_material(self):
        self.thermoforming_data.material = self.material1
        self.thermoforming_data.save()
        self.permeability_data.thermoforming_id = self.thermoforming_data
        try:
            self.permeability_data.save()  # This should not raise any error
        except ValidationError:
            self.fail("Unexpected ValidationError")
