from django.db import models
from django.core.exceptions import ValidationError

class ColdformingStamp(models.Model):
    name = models.CharField(max_length=200, unique=True)
    friction_coefficient = models.FloatField()

    def units(self, quantity):
        units = {"friction_coefficient": "<>"}
        return units.get(quantity, "")

    def __str__(self):
        return f"({self.id}).{self.name}"

class Material(models.Model):
    name = models.CharField(max_length=200, unique=True)
    thickness = models.FloatField()

    def units(self, quantity):
        units = {"thickness": "µm"}
        return units.get(quantity, "")

    def __str__(self):
        return f"({self.id}).{self.name}"
    
class LayerStructure(models.Model):
    name = models.CharField(max_length=200, unique=True)
    released_for_thermoforming = models.BooleanField(default=False)
    released_for_thermoforming_lid = models.BooleanField(default=False)
    released_for_coldforming = models.BooleanField(default=False)

    def __str__(self):
        return f"({self.id}).{self.name}"

    def is_available_for_thermoforming(self):
        material_orders = MaterialOrder.objects.filter(layer_structure=self)
        for material_order in material_orders:
            material = material_order.material
            if not hasattr(material, 'thermoforming_data'):
                return False
            if not material.thermoforming_data.is_data_complete():
                return False
        return True
    
    def is_available_for_thermoforming_lid(self):
        material_orders = MaterialOrder.objects.filter(layer_structure=self)
        for material_order in material_orders:
            material = material_order.material
            if not hasattr(material, 'thermoforminglid_data'):
                return False
            if not material.thermoforminglid_data.is_data_complete():
                return False
           
        return True
    
    def is_available_for_coldforming(self):
        material_orders = MaterialOrder.objects.filter(layer_structure=self)
        for material_order in material_orders:
            material = material_order.material
            if not hasattr(material, 'coldforming_data'):
                return False
            if not material.coldforming_data.is_data_complete():
                return False
        return True
    
class MaterialOrder(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    layer_structure = models.ForeignKey(LayerStructure, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ['material', 'layer_structure', 'order']
    
    def __str__(self):
        return f"({self.material.id}).{self.material.name}"

class ThermoformingData(models.Model):
    material = models.OneToOneField(Material, related_name='thermoforming_data', on_delete=models.CASCADE)
    wvtr_data = models.ManyToManyField('WVTRData')
    otr_data = models.ManyToManyField('OTRData')
    density_data = models.ManyToManyField('DensityData')
    youngs_modulus_data = models.ManyToManyField('YoungsModulusData')
    tensile_curve_data = models.ManyToManyField('TensileCurveData')

    def save(self, *args, **kwargs):
        # Only perform the validation check if this is an existing record
        if self.id:
            # Validate that each related data point is connected to the same Material as this ThermoformingData instance
            for data_set in [
                self.wvtr_data.all(),
                self.otr_data.all(),
                self.density_data.all(),
                self.youngs_modulus_data.all(),
                self.tensile_curve_data.all()
            ]:
                for data_point in data_set:
                    if data_point.material != self.material:
                        raise ValidationError(f"Data point {data_point} is not linked to the same material as this ThermoformingData instance.")

        super(ThermoformingData, self).save(*args, **kwargs)
    
    def is_data_complete(self):
        return all([
            self.wvtr_data.exists(),
            self.otr_data.exists(),
            self.density_data.exists(),
            self.youngs_modulus_data.exists(),
            self.tensile_curve_data.exists()
        ])

    def get_associated_wvtr_data(self):
        return self.wvtr_data.all()
    
    def get_associated_otr_data(self):
        return self.otr_data.all()
    
    def get_associated_density_data(self):
        return self.density_data.all()
    
    def get_associated_youngs_modulus_data(self):
        return self.youngs_modulus_data.all()
    
    def get_associated_tensile_data(self):
        curves = self.tensile_curve_data.all()  
        curve_data = []
        for curve in curves:
            points = TensileCurvePoint.objects.filter(tensile_curve=curve)
            stresses = [point.stress for point in points]
            strains = [point.strain for point in points]
            curve_data.append({
                'strain_rate': curve.strain_rate,
                'temperature': curve.temperature,
                'direction': curve.direction,
                'stresses': stresses,
                'strains': strains,
                'pk': curve.pk
            })
        return curve_data

class ColdformingData(models.Model):
    material = models.OneToOneField(Material, related_name='coldforming_data', on_delete=models.CASCADE)
    youngs_modulus_data = models.ManyToManyField('YoungsModulusData')
    tensile_curve_data = models.ManyToManyField('TensileCurveData')
    drucker_prager_curve_data = models.ManyToManyField('DruckerPragerCurveData')

    def save(self, *args, **kwargs):
        # Only perform the validation check if this is an existing record
        if self.id:
            # Validate that each related data point is connected to the same Material as this ColdformingData instance
            for data_set in [
                self.youngs_modulus_data.all(),
                self.tensile_curve_data.all(),
                self.drucker_prager_curve_data.all()
            ]:
                for data_point in data_set:
                    if data_point.material != self.material:
                        raise ValidationError(f"Data point {data_point} is not linked to the same material as this ColdformingData instance.")

        super(ColdformingData, self).save(*args, **kwargs)
    
    def is_data_complete(self):
        return all([
            self.youngs_modulus_data.exists(),
            self.tensile_curve_data.exists(),
            self.drucker_prager_curve_data.exists()
        ])
    
    def get_associated_youngs_modulus_data(self):
        return self.youngs_modulus_data.all()
    
    def get_associated_tensile_data(self):
        curves = self.tensile_curve_data.all()  
        curve_data = []
        for curve in curves:
            points = TensileCurvePoint.objects.filter(tensile_curve=curve)
            stresses = [point.stress for point in points]
            strains = [point.strain for point in points]
            curve_data.append({
                'strain_rate': curve.strain_rate,
                'temperature': curve.temperature,
                'direction': curve.direction,
                'stresses': stresses,
                'strains': strains,
                'pk': curve.pk
            })
        return curve_data
    def get_associated_drucker_prager_data(self):
        curves = self.drucker_prager_curve_data.all()  
        curve_data = []
        for curve in curves:
            points = DruckerPragerCurvePoint.objects.filter(drucker_prager_curve=curve)
            stresses = [point.stress for point in points]
            strains = [point.strain for point in points]
            curve_data.append({
                'input1': curve.input1,
                'input2': curve.input2,
                'input3': curve.input3,
                'direction': curve.direction,
                'stresses': stresses,
                'strains': strains,
                'pk': curve.pk
            })
        return curve_data

class ThermoformingLidData(models.Model):
    material = models.OneToOneField(Material, related_name='thermoforminglid_data', on_delete=models.CASCADE)
    wvtr_data = models.ManyToManyField('WVTRData')
    otr_data = models.ManyToManyField('OTRData')

    def save(self, *args, **kwargs):
        # Only perform the validation check if this is an existing record
        if self.id:
            # Validate that each related data point is connected to the same Material as this ThermoformingLidData instance
            for data_set in [
                self.wvtr_data.all(),
                self.otr_data.all(),
            ]:
                for data_point in data_set:
                    if data_point.material != self.material:
                        raise ValidationError(f"Data point {data_point} is not linked to the same material as this ThermoformingLidData instance.")

        super(ThermoformingLidData, self).save(*args, **kwargs)
    
    def is_data_complete(self):
        return all([
            self.wvtr_data.exists(),
            self.otr_data.exists(),
        ])

    def get_associated_wvtr_data(self):
        return self.wvtr_data.all()
    
    def get_associated_otr_data(self):
        return self.otr_data.all()
       
class WVTRData(models.Model):
    material = models.ForeignKey(Material, related_name='wvtr_data', on_delete=models.CASCADE)
    temperature = models.FloatField()
    RH = models.FloatField()
    WVTR = models.FloatField()
    diffusivity = models.FloatField(null=True, default=None)
    solubility = models.FloatField(null=True, default=None)

    def __str__(self):
        return f"({self.id})={self.WVTR}{self.units('WVTR')} (RH={self.RH}{self.units('RH')}, T={self.temperature}{self.units('temperature')})"
    
    def units(self, quantity):
        units = {
            "temperature":"°C",
            "RH":"%",
            "WVTR":"<>",
            "diffusivity":"<>",
            "solubility":"<>"
        }
        return units.get(quantity, "")

class OTRData(models.Model):
    material = models.ForeignKey(Material, related_name='otr_data', on_delete=models.CASCADE)
    temperature = models.FloatField()
    RH = models.FloatField()
    OTR = models.FloatField()
    diffusivity = models.FloatField(null=True, default=None)
    solubility = models.FloatField(null=True, default=None)

    def __str__(self):
        return f"({self.id})={self.OTR}{self.units('OTR')} (RH={self.RH}{self.units('RH')}, T={self.temperature}{self.units('temperature')})"
    
    def units(self, quantity):
        units = {
            "temperature":"°C",
            "RH":"%",
            "OTR":"<>",
            "diffusivity":"<>",
            "solubility":"<>"
        }
        return units.get(quantity, "")

class DensityData(models.Model):
    material = models.ForeignKey(Material, related_name='density_data', on_delete=models.CASCADE)
    density = models.FloatField()
    temperature = models.FloatField()

    def __str__(self):
        return f"({self.id}).{self.density}{self.units('density')} ({self.temperature}{self.units('temperature')})"
    
    def units(self, quantity):
        units = {
            "density":"<>",
            "temperature":"°C",
        }
        return units.get(quantity, "")

class YoungsModulusData(models.Model):
    material = models.ForeignKey(Material, related_name='youngs_modulus_data', on_delete=models.CASCADE)
    youngs_modulus = models.FloatField()
    poissons_ratio = models.FloatField()
    temperature = models.FloatField()
    DIRECTION_CHOICES = [
        ('MD', 'MD'),
        ('CD', 'CD'),
    ]
    direction = models.CharField(max_length=2, choices=DIRECTION_CHOICES)

    def __str__(self):
        return f"({self.id}).{self.direction} - YM={self.youngs_modulus}{self.units('youngs_modulus')}, PR={self.poissons_ratio}{self.units('poissons_ratio')}, T={self.temperature}{self.units('temperature')}"
    
    def units(self, quantity):
        units = {
            "youngs_modulus":"<>",
            "poissons_ratio":"<>",
            "temperature":"°C",
        }
        return units.get(quantity, "")

class TensileCurveData(models.Model):
    material = models.ForeignKey(Material, related_name='tensile_curve_data', on_delete=models.CASCADE)
    strain_rate = models.FloatField()
    temperature= models.FloatField()
    DIRECTION_CHOICES = [
        ('MD', 'MD'),
        ('CD', 'CD'),
    ]
    direction = models.CharField(max_length=2, choices=DIRECTION_CHOICES)

    def __str__(self):
        return f"({self.id}).{self.direction} - SR={self.strain_rate}{self.units('strain_rate')}, T={self.temperature}{self.units('temperature')}"
    
    def units(self, quantity):
        units = {
            "strain_rate":"<>",
            "temperature":"°C",
        }
        return units.get(quantity, "")

class TensileCurvePoint(models.Model):
    tensile_curve = models.ForeignKey(TensileCurveData, on_delete=models.CASCADE)
    stress = models.FloatField()
    strain = models.FloatField()

    def units(self, quantity):
        units = {
            "stress":"<>",
            "strain":"<>",
        }
        return units.get(quantity, "")


class DruckerPragerCurveData(models.Model):
    material = models.ForeignKey(Material, related_name='drucker_prager_curve_data', on_delete=models.CASCADE)
    input1 = models.FloatField()
    input2 = models.FloatField()
    input3 = models.FloatField()
    DIRECTION_CHOICES = [
        ('MD', 'MD'),
        ('CD', 'CD'),
    ]
    direction = models.CharField(max_length=2, choices=DIRECTION_CHOICES)
    def __str__(self):
        return f"({self.id}).{self.direction} - input1={self.input1}{self.units('input1')}, input2={self.input2}{self.units('input2')}, input3={self.input3}{self.units('input3')}"
    
    def units(self, quantity):
        units = {
            "input1":"<>",
            "input2":"<>",
            "input3":"<>"
        }
        return units.get(quantity, "")

class DruckerPragerCurvePoint(models.Model):
    drucker_prager_curve = models.ForeignKey(DruckerPragerCurveData, on_delete=models.CASCADE)
    stress = models.FloatField()
    strain = models.FloatField()

    def units(self, quantity):
        units = {
            "stress":"<>",
            "strain":"<>",
        }
        return units.get(quantity, "")