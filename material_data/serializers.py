from rest_framework import serializers
from .models import ThermoformingData, ThermoformingLidData, ColdformingData

class ThermoformingDataSerializer(serializers.ModelSerializer):
    material_id = serializers.SerializerMethodField()
    material_name = serializers.SerializerMethodField()
    thickness = serializers.SerializerMethodField()
    wvtr = serializers.SerializerMethodField()
    otr = serializers.SerializerMethodField()
    density = serializers.SerializerMethodField()
    youngs_modulus = serializers.SerializerMethodField()
    tensile_lines = serializers.SerializerMethodField()
    tensile_points = serializers.SerializerMethodField()

    class Meta:
        model = ThermoformingData
        fields = [
            'material_id', 'id', 'material_name', 'thickness', 
            'wvtr', 'otr',  'density', 'youngs_modulus','tensile_points', 'tensile_lines'
        ]

    def get_material_id(self, obj):
        return obj.material.id

    def get_material_name(self, obj):
        return obj.material.name

    def get_thickness(self, obj):
        return obj.material.thickness

    def get_wvtr(self, obj):
        return [
            {
                'temperature': data.temperature,
                'RH': data.RH,
                'wvtr': data.WVTR
            }
            for data in obj.get_associated_wvtr_data()
        ]
    def get_otr(self, obj):
        return [
            {
                'temperature': data.temperature,
                'RH': data.RH,
                'otr': data.OTR
            }
            for data in obj.get_associated_otr_data()
        ]

    def get_density(self, obj):
        return [
            {
                'temperature': data.temperature,
                'density': data.density
            }
            for data in obj.get_associated_density_data()
        ]

    def get_youngs_modulus(self, obj):
        return [
            {
                'direction': data.direction,
                'youngs_modulus': data.youngs_modulus,
                'poissons_ratio': data.poissons_ratio,
                'temperature': data.temperature
            }
            for data in obj.get_associated_youngs_modulus_data()
        ]
    
    def get_tensile_points(self, obj):
        points = []
        for curve in obj.get_associated_tensile_data():
            direction = curve['direction']
            strain_rate = curve['strain_rate']
            temperature = curve['temperature']

            # Zip stresses and strains together to form pairs
            stress_strain_pairs = zip(curve['stresses'], curve['strains'])

            for stress, strain in stress_strain_pairs:
                point = {
                    'direction': direction,
                    'stress': stress,
                    'strain': strain,
                    'strain_rate': strain_rate,
                    'temperature': temperature,
                }
                points.append(point)

        return points
    
    def get_tensile_lines(self, obj):
        return [
           {
                'direction': curve['direction'],
                'stress': curve['stresses'],  # Assuming this is how you named it in your dict
                'strain': curve['strains'],  # Assuming this is how you named it in your dict
                'strain_rate': curve['strain_rate'],
                'temperature': curve['temperature']
            }
            for curve in obj.get_associated_tensile_data()
        ]

class ColdformingDataSerializer(serializers.ModelSerializer):
    material_id = serializers.SerializerMethodField()
    material_name = serializers.SerializerMethodField()
    thickness = serializers.SerializerMethodField()
    youngs_modulus = serializers.SerializerMethodField()
    tensile_lines = serializers.SerializerMethodField()
    drucker_prager_lines = serializers.SerializerMethodField()

    class Meta:
        model = ColdformingData
        fields = [
            'material_id', 'id', 'material_name', 'thickness', 
            'youngs_modulus', 'tensile_lines', 'drucker_prager_lines'
        ]

    def get_material_id(self, obj):
        return obj.material.id

    def get_material_name(self, obj):
        return obj.material.name

    def get_thickness(self, obj):
        return obj.material.thickness

    def get_youngs_modulus(self, obj):
        return [
            {
                'direction': data.direction,
                'youngs_modulus': data.youngs_modulus,
                'poissons_ratio': data.poissons_ratio,
                'temperature': data.temperature
            }
            for data in obj.get_associated_youngs_modulus_data()
        ]
    
    def get_tensile_lines(self, obj):
        return [
           {
                'direction': curve['direction'],
                'stress': curve['stresses'],
                'strain': curve['strains'],  
                'strain_rate': curve['strain_rate'],
                'temperature': curve['temperature']
            }
            for curve in obj.get_associated_tensile_data()
        ]
    def get_drucker_prager_lines(self, obj):
        return [
           {
                'direction': curve['direction'],
                'stress': curve['stresses'],
                'strain': curve['strains'],  
                'input1': curve['input1'],
                'input2': curve['input2'],
                'input3': curve['input3']
            }
            for curve in obj.get_associated_drucker_prager_data()
        ]
    
class ThermoformingLidDataSerializer(serializers.ModelSerializer):
    material_id = serializers.SerializerMethodField()
    material_name = serializers.SerializerMethodField()
    thickness = serializers.SerializerMethodField()
    wvtr = serializers.SerializerMethodField()
    otr = serializers.SerializerMethodField()

    class Meta:
        model = ThermoformingLidData
        fields = [
            'material_id', 'id', 'material_name', 'thickness', 
            'wvtr', 'otr'
        ]

    def get_material_id(self, obj):
        return obj.material.id

    def get_material_name(self, obj):
        return obj.material.name

    def get_thickness(self, obj):
        return obj.material.thickness

    def get_wvtr(self, obj):
        return [
            {
                'temperature': data.temperature,
                'RH': data.RH,
                'wvtr': data.WVTR
            }
            for data in obj.get_associated_wvtr_data()
        ]
    def get_otr(self, obj):
        return [
            {
                'temperature': data.temperature,
                'RH': data.RH,
                'otr': data.OTR
            }
            for data in obj.get_associated_otr_data()
        ]