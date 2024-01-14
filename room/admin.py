from django.contrib import admin
from . import models

# Register your models here.
class BedTypeAdmin(admin.ModelAdmin):
      prepopulated_fields = {'slug': ('name',)}
class RoomFeaturesAdmin(admin.ModelAdmin):
      prepopulated_fields = {'slug': ('name',)}
class RoomFacilitiesAdmin(admin.ModelAdmin):
      prepopulated_fields = {'slug': ('name',)}
      
admin.site.register(models.BedType, BedTypeAdmin)
admin.site.register(models.Features, RoomFeaturesAdmin)
admin.site.register(models.RoomFacilities, RoomFacilitiesAdmin)
admin.site.register(models.Room)
