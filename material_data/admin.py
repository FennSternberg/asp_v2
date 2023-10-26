from django.contrib import admin
from .models import Material, WVTRData

admin.site.register(Material)
admin.site.register(WVTRData)  # Register the new model
