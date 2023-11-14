from django.urls import path
from . import views

urlpatterns = [
     path('guide/', views.guide, name='material_guide'),


    path('api/thermoformingdata//<int:pk>/', views.ThermoformingDataAPI.as_view(), name='thermoformingdata_api'),
    path('api/coldformingdata//<int:pk>/', views.ColdformingDataAPI.as_view(), name='coldformingdata_api'),
    path('api/thermoformingliddata//<int:pk>/', views.ThermoformingLidDataAPI.as_view(), name='thermoformingliddata_api'),

    path('', views.MaterialListView.as_view(), name='material_list'),
    path('new/', views.MaterialCreateView.as_view(), name='material_create'),
    path('<int:pk>/edit/', views.MaterialUpdateView.as_view(), name='material_update'),
    path('<int:pk>/delete/', views.MaterialDeleteView.as_view(), name='material_delete'),

    path('coldformingstamp/', views.ColdformingStampListView.as_view(), name='coldformingstamp_list'),
    path('coldformingstamp/new/', views.ColdformingStampCreateView.as_view(), name='coldformingstamp_create'),
    path('coldformingstamp/<int:pk>/edit/', views.ColdformingStampUpdateView.as_view(), name='coldformingstamp_update'),
    path('coldformingstamp/<int:pk>/delete/', views.ColdformingStampDeleteView.as_view(), name='coldformingstamp_delete'), 

    path('thermoformingplug/', views.ThermoformingPlugListView.as_view(), name='thermoformingplug_list'),
    path('thermoformingplug/new/', views.ThermoformingPlugCreateView.as_view(), name='thermoformingplug_create'),
    path('thermoformingplug/<int:pk>/edit/', views.ThermoformingPlugUpdateView.as_view(), name='thermoformingplug_update'),
    path('thermoformingplug/<int:pk>/delete/', views.ThermoformingPlugDeleteView.as_view(), name='thermoformingplug_delete'), 

    path('layer_structure/', views.LayerStructureListView.as_view(), name='layerstructure_list'),
    path('layer_structure/new/', views.LayerStructureCreateView.as_view(), name='layerstructure_create'),
    path('layer_structure/<int:pk>/edit/', views.LayerStructureUpdateView.as_view(), name='layerstructure_update'),
    path('layer_structure/<int:pk>/delete/', views.LayerStructureDeleteView.as_view(), name='layerstructure_delete'), 
   
    
    path('wvtrdata/', views.WVTRDataListView.as_view(), name='wvtrdata_list'),
    path('wvtrdata/new/', views.WVTRDataCreateView.as_view(), name='wvtrdata_create'),
    path('wvtrdata/<int:pk>/edit/', views.WVTRDataUpdateView.as_view(), name='wvtrdata_update'),
    path('wvtrdata/<int:pk>/delete/', views.WVTRDataDeleteView.as_view(), name='wvtrdata_delete'),

    path('otrdata/', views.OTRDataListView.as_view(), name='otrdata_list'),
    path('otrdata/new/', views.OTRDataCreateView.as_view(), name='otrdata_create'),
    path('otrdata/<int:pk>/edit/', views.OTRDataUpdateView.as_view(), name='otrdata_update'),
    path('otrdata/<int:pk>/delete/', views.OTRDataDeleteView.as_view(), name='otrdata_delete'),
    
    path('densitydata/', views.DensityDataListView.as_view(), name='densitydata_list'),
    path('densistydata/new/', views.DensityDataCreateView.as_view(), name='densitydata_create'),
    path('densistydata/<int:pk>/edit/', views.DensityDataUpdateView.as_view(), name='densitydata_update'),
    path('densitydata/<int:pk>/delete/', views.DensityDataDeleteView.as_view(), name='densitydata_delete'),
    
    
    path('youngsmodulusdata/', views.YoungsModulusDataListView.as_view(), name='youngsmodulusdata_list'),
    path('youngsmodulusdata/new/', views.YoungsModulusDataCreateView.as_view(), name='youngsmodulusdata_create'),
    path('youngsmodulusdata/<int:pk>/edit/', views.YoungsModulusDataUpdateView.as_view(), name='youngsmodulusdata_update'),
    path('youngsmodulusdata/<int:pk>/delete/', views.YoungsModulusDataDeleteView.as_view(), name='youngsmodulusdata_delete'),

    path('tensilecurvedata/', views.TensileCurveDataListView.as_view(), name='tensilecurvedata_list'),
    path('tensilecurvedata/new/', views.TensileCurveDataCreateView.as_view(), name='tensilecurvedata_create'),
    path('tensilecurvedata/<int:pk>/edit/', views.TensileCurveDataUpdateView.as_view(), name='tensilecurvedata_update'),
    path('tensilecurvedata/<int:pk>/delete/', views.TensileCurveDataDeleteView.as_view(), name='tensilecurvedata_delete'),

    path('druckerpragercurvedata/', views.DruckerPragerCurveDataListView.as_view(), name='druckerpragercurvedata_list'),
    path('druckerpragercurvedata/new/', views.DruckerPragerCurveDataCreateView.as_view(), name='druckerpragercurvedata_create'),
    path('druckerpragercurvedata/<int:pk>/edit/', views.DruckerPragerCurveDataUpdateView.as_view(), name='druckerpragercurvedata_update'),
    path('druckerpragercurvedata/<int:pk>/delete/', views.DruckerPragerCurveDataDeleteView.as_view(), name='druckerpragercurvedata_delete'),
    
    path('thermoformingdata/', views.ThermoformingDataListView.as_view(), name='thermoformingdata_list'),
    path('thermoformingdata/new/', views.ThermoformingDataCreateView.as_view(), name='thermoformingdata_create'),
    path('thermoformingdata/<int:pk>/edit', views.ThermoformingDataUpdateView.as_view(), name='thermoformingdata_update'),
    path('thermoformingdata/<int:pk>/delete/', views.ThermoformingDataDeleteView.as_view(), name='thermoformingdata_delete'),
    path('thermoformingdata/<int:pk>/', views.ThermoformingDataDetailView.as_view(), name='thermoformingdata_detail'),

    path('thermoformingliddata/', views.ThermoformingLidDataListView.as_view(), name='thermoformingliddata_list'),
    path('thermoformingliddata/new/', views.ThermoformingLidDataCreateView.as_view(), name='thermoformingliddata_create'),
    path('thermoformingliddata/<int:pk>/edit', views.ThermoformingLidDataUpdateView.as_view(), name='thermoformingliddata_update'),
    path('thermoformingliddata/<int:pk>/delete/', views.ThermoformingLidDataDeleteView.as_view(), name='thermoformingliddata_delete'),
    path('thermoformingliddata/<int:pk>/', views.ThermoformingLidDataDetailView.as_view(), name='thermoformingliddata_detail'),

    path('coldformingdata/', views.ColdformingDataListView.as_view(), name='coldformingdata_list'),
    path('coldformingdata/new/', views.ColdformingDataCreateView.as_view(), name='coldformingdata_create'),
    path('coldformingdata/<int:pk>/edit', views.ColdformingDataUpdateView.as_view(), name='coldformingdata_update'),
    path('coldformingdata/<int:pk>/delete/', views.ColdformingDataDeleteView.as_view(), name='coldformingdata_delete'),
    path('coldformingdata/<int:pk>/', views.ColdformingDataDetailView.as_view(), name='coldformingdata_detail'),
]  
