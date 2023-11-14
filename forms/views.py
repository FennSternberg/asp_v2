from django.shortcuts import render, redirect

from django.core.exceptions import ValidationError
from .geometry_check import calc_R, calc_R2 as calc_Rf, sketch_geometry
from django.contrib.auth.models import User
from material_data.models import LayerStructure, ThermoformingPlug
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AnalysisDetailSerializer, ShapeAndProfileSerializer, CavityGeometrySerializer, MaterialDetailSerializer
from .models import ThermoformingCavityParameters
def Thermoforming(request):
    internal_contact_choices = [
        {"value": user.id, "label": str(user)}
        for user in User.objects.all()
    ]

    available_materials = [
        {"value":layer_structure.id, "label":str(layer_structure)}
        for layer_structure in LayerStructure.objects.all()
        if layer_structure.is_available_for_thermoforming()
    ]

    available_lids = [
        {"value":layer_structure.id, "label":str(layer_structure)}
        for layer_structure in LayerStructure.objects.all()
        if layer_structure.is_available_for_thermoforming_lid()
    ]

    available_plugs = [
        {"value": plug_material.id, "label":str(plug_material)}
        for plug_material in ThermoformingPlug.objects.all()
    ]

    shape_choices = ThermoformingCavityParameters().get_shape_choices()
    profile_choices = ThermoformingCavityParameters().get_profile_choices()

    context = {
        "internal_contact_choices": internal_contact_choices,
        "current_user_id": request.user.id if request.user.is_authenticated else None,
        "available_materials": available_materials,
        "available_lids": available_lids,
        "shape_choices":shape_choices,
        "profile_choices":profile_choices,
        "available_plugs":available_plugs
    }
    return render(request, 'thermoforming_verification.html', context)

class ValidatePlug(APIView):
    def post(self,request):
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class ValidateAnalysisDetails(APIView):
    def post(self, request):
        print(f"Received data: {request.data}")
        serializer = AnalysisDetailSerializer(data=request.data)
        if serializer.is_valid():
            print('Serializer is valid')
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            print('Serializer is not valid')
            print(f"Serializer errors: {serializer.errors}")
            return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_200_OK)

class ValidateMaterialDetails(APIView):
    def post(self, request):
        print(f"Received data: {request.data}")
        serializer = MaterialDetailSerializer(data=request.data)
        if serializer.is_valid():
            print('Serializer is valid')
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            print('Serializer is not valid')
            print(f"Serializer errors: {serializer.errors}")
            return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_200_OK)

class ValidateShapeAndProfile(APIView):
    def post(self, request):
        print(f"Received data: {request.data}") 
        serializer = ShapeAndProfileSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            print('Serializer is valid')
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            print('Serializer is not valid')
            print(f"Serializer errors: {serializer.errors}")
            return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_200_OK)

class ValidateCavityGeometry(APIView):
    def post(self, request):
        print(f"Received data: {request.data}")
        if "rf" not in request.data or request.data['rf']=="":
            print("Rf not in data")
            request.data['profile'] = 'profile1' # change profile to profile1
            serializer = CavityGeometrySerializer(data=request.data)
            if serializer.is_valid():
                # Try to make a profile 1 cavity
                print('Serializer is valid when profile is changed to profile 1')
                request.data['rb'] = round(calc_R(float(request.data['c1']), float(request.data['wall_angle']), float(request.data['depth']), float(request.data['r'])),2)
                sketch_points = self.get_sketch_data(request)
                return Response({'status': 'success','updated_data': request.data,'sketch_points':sketch_points}, status=status.HTTP_200_OK)
            else:
                # Profile 1 cavity was not possible, instead try profile 3 cavity with default value
                if 'w' in request.data and 'wall_angle' in request.data and 'profile' in request.data:
                    request.data['rf'] = round(calc_Rf(float(request.data['w']), float(request.data['wall_angle'])),2)
                    request.data['profile'] = "profile3"
                serializer = CavityGeometrySerializer(data=request.data)
                if serializer.is_valid():
                    sketch_points = self.get_sketch_data(request)
                    print("Serializer is valid with a default value of Rf")
                    return Response({'status': 'success','updated_data': request.data,'sketch_points':sketch_points}, status=status.HTTP_200_OK)
                else:
                    print('Serializer is not valid')
                    print(f"Serializer errors: {serializer.errors}")
                    return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_200_OK)
        else:
            serializer = CavityGeometrySerializer(data=request.data)

            if serializer.is_valid():
                sketch_points = self.get_sketch_data(request)
                print('Serializer is valid')
                return Response({'status': 'success','sketch_points':sketch_points}, status=status.HTTP_200_OK)
            else:
                print('Serializer is not valid')
                print(f"Serializer errors: {serializer.errors}")
                return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_200_OK)
    
    def get_sketch_data(self,request):
        try:
            profile = request.data.get('profile')
            shape = request.data.get('shape')
            c1 = float(request.data.get('c1'))
            if profile != "profile2":
                rb = float(request.data.get('rb'))
            else:
                rb = ""
            if profile != "profile1":
                rf = float(request.data.get('rf'))
            else:
                rf = ""
            
            if shape == "oblong":
                c2 = float(request.data.get('c2'))
            else:
                c2 = ""
                
            wall_angle = float(request.data.get('wall_angle'))
            r = float(request.data.get('r'))
            depth = float(request.data.get('depth'))
            x_sketch, y_sketch, x_long_sketch, y_long_sketch = sketch_geometry(profile, c1, rb, rf, wall_angle, r, depth, shape, c2)
            return [list(zip(x_sketch, y_sketch)), list(zip(x_long_sketch, y_long_sketch))]
        except Exception as e:
            print(e)
            return [[],[]]

        



