from django.urls import path
from . import views

urlpatterns = [
    path('api/thermoformingdata/<int:thermoforming_id>/', views.ThermoformingDataAPI.as_view(), name='thermoformingdata_api'),

    path('', views.MaterialListView.as_view(), name='material_list'),
    path('new/', views.MaterialCreateView.as_view(), name='material_create'),
    path('<int:pk>/edit/', views.MaterialUpdateView.as_view(), name='material_update'),
    path('<int:pk>/delete/', views.MaterialDeleteView.as_view(), name='material_delete'),

    path('layer_structure/', views.LayerStructureListView.as_view(), name='layerstructure_list'),
    path('layer_structure/new/', views.LayerStructureCreateView.as_view(), name='layerstructure_create'),
    # path('layer_structure/<int:pk>/edit/', views.LayerStructureListView.as_view(), name='layer_structure_update'),
    path('layer_structure/<int:pk>/delete/', views.LayerStructureDeleteView.as_view(), name='layerstructure_delete'), 
   
    
    path('wvtrdata/', views.WVTRDataListView.as_view(), name='wvtrdata_list'),
    path('wvtrdata/new/', views.WVTRDataCreateView.as_view(), name='wvtrdata_create'),
    path('wvtrdata/<int:pk>/edit/', views.WVTRDataUpdateView.as_view(), name='wvtrdata_update'),
    path('wvtrdata/<int:pk>/delete/', views.WVTRDataDeleteView.as_view(), name='wvtrdata_delete'),
    
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
    
    path('thermoformingdata/', views.ThermoformingDataListView.as_view(), name='thermoformingdata_list'),
    path('thermoformingdata/new/', views.ThermoformingDataCreateView.as_view(), name='thermoformingdata_create'),
    path('thermoformingdata/<int:pk>/edit', views.ThermoformingDataUpdateView.as_view(), name='thermoformingdata_update'),
    path('thermoformingdata/<int:pk>/delete/', views.ThermoformingDataDeleteView.as_view(), name='thermoformingdata_delete'),
    path('thermoformingdata/<int:pk>/', views.ThermoformingDataDetailView.as_view(), name='thermoformingdata_detail'),
] 
