from django.shortcuts import render, redirect

from django.core.exceptions import ValidationError
from .geometry_check import calc_R, calc_R2 as calc_Rf
from django.contrib.auth.models import User
from material_data.models import LayerStructure
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AnalysisDetailSerializer, ShapeAndProfileSerializer, CavityGeometrySerializer, MaterialDetailSerializer

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

    context = {
        "internal_contact_choices": internal_contact_choices,
        "current_user_id": request.user.id if request.user.is_authenticated else None,
        "available_materials": available_materials,
        "available_lids": available_lids
    }
    return render(request, 'thermoforming_verification.html', context)

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
                return Response({'status': 'success','updated_data': request.data}, status=status.HTTP_200_OK)
            else:
                # Profile 1 cavity was not possible, instead try profile 3 cavity with default value
                if 'w' in request.data and 'wall_angle' in request.data and 'profile' in request.data:
                    request.data['rf'] = round(calc_Rf(float(request.data['w']), float(request.data['wall_angle'])),2)
                    request.data['profile'] = "profile3"
                serializer = CavityGeometrySerializer(data=request.data)
                if serializer.is_valid():
                    print("Serializer is valid with a default value of Rf")
                    return Response({'status': 'success','updated_data': request.data}, status=status.HTTP_200_OK)
                else:
                    print('Serializer is not valid')
                    print(f"Serializer errors: {serializer.errors}")
                    return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_200_OK)
        else:
            serializer = CavityGeometrySerializer(data=request.data)
            if serializer.is_valid():
                print('Serializer is valid')
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                print('Serializer is not valid')
                print(f"Serializer errors: {serializer.errors}")
                return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_200_OK)
        



