from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('validate_analysis_details/', views.ValidateAnalysisDetails.as_view(), name='validate_analysis_details'),
    path('validate_shape_and_profile/', views.ValidateShapeAndProfile.as_view(), name='validate_shape_and_profile'),
    path('validate_cavity_geometry/', views.ValidateCavityGeometry.as_view(), name='validate_cavity_geometry'),
    path('thermoforming-verification/', views.Thermoforming, name='thermoforming_form'),
]
  