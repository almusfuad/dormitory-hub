from django.contrib import admin
from . import models

# Register your models here.
#prepopulated_fields
class LocationAdmin(admin.ModelAdmin):
      prepopulated_fields = {'slug': ('name',)}      
class FacilitiesAdmin(admin.ModelAdmin):
      prepopulated_fields = {'slug': ('name',)}
class HotelAdmin(admin.ModelAdmin):
      prepopulated_fields = {'slug': ('name',)}

      
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Facilities, FacilitiesAdmin)
admin.site.register(models.Hotel, HotelAdmin)