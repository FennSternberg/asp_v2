from rest_framework import serializers
from .models import AnalysisDetail, ThermoformingCavityParameters
from .geometry_check import valid_profile1, valid_profile2, valid_profile3, calc_R, calc_R2 as calc_Rf

def custom_is_input(required_fields, data):
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError({field: "This field is required"})
    
class AnalysisDetailSerializer(serializers.ModelSerializer):
  

    class Meta:
        model = AnalysisDetail
        fields = ['jobname', 'customer', 'internal_contact']

class CavityGeometrySerializer(serializers.ModelSerializer):
    c1 = serializers.FloatField(required=False)
    l = serializers.FloatField(required=False)
    class Meta:
        model = ThermoformingCavityParameters
        fields = ['w', 'c1', 'l', 'c2', 'depth', 'wall_angle', 'r', 'rf', 'rb','profile','shape']

    def validate(self, data):
        profile = data.get('profile', None)
        shape = data.get('shape', None)
        if shape=="oblong":
            custom_is_input(["l","c1"], data)
        
        if profile == "profile2":
            custom_is_input(["rf"], data)

        # Type validation
        for key, value in data.items():
            if key not in ['profile','shape']:
                if not isinstance(value, (int, float)):
                    raise serializers.ValidationError({key: "Must be a number"})
            else:
                if not isinstance(value, str):
                    raise serializers.ValidationError({key: "Must be a string"})
                
        err = 0.01  # Example error tolerance, you can replace it with the actual value
        error_message = "These parameters can not form a physically valid geometry"

        if profile == 'profile1':
            if not valid_profile1(data['rb'], data['wall_angle'], data['c1'], data['depth'], data['r'], err):
                raise serializers.ValidationError({"rb": error_message,
                                                   "wall_angle":  error_message,
                                                   "c1":  error_message,
                                                   "depth":  error_message,
                                                   "r":  error_message,})
                
        elif profile == 'profile2':
            if not valid_profile2(data['c1'], data['rf'], data['wall_angle'], data['r'], data['depth']):
                raise serializers.ValidationError({"c1":  error_message,
                                                   "rf":  error_message,
                                                   "wall_angle":  error_message,
                                                   "r":  error_message,
                                                   "depth":  error_message})

        elif profile == 'profile3':
            if not valid_profile3(data['rb'], data['rf'], data['wall_angle'], data['c1'], data['depth'], data['r']):
                raise serializers.ValidationError({"rb":  error_message, 
                                                   "rf":  error_message,
                                                   "wall_angle":  error_message,
                                                   "c1":  error_message,
                                                   "depth":  error_message,
                                                   "r":  error_message})        
        else:
            raise serializers.ValidationError({"profile": "Invalid profile type"})

        return data  

class ShapeAndProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThermoformingCavityParameters
        fields = ["shape", "profile"]
    shape = serializers.ChoiceField(choices=['round', 'oblong'])
    profile = serializers.ChoiceField(choices=['profile2', 'profile3']) 

    def validate_shape(self, value):
        if value is None:
            raise serializers.ValidationError("Shape must be selected.")
        return value

    def validate_profile(self, value):
        if value is None:
            raise serializers.ValidationError("Profile must be selected.") 
        return value
