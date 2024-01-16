from django.contrib import admin
from . import models

# Register your models here.
class LocationAdmin(admin.ModelAdmin):
      prepopulated_fields = {'slug': ('location',), }
class DormitoryAdmin(admin.ModelAdmin):
      prepopulated_fields = { 'slug': ('name',),}
      
admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Dormitory, DormitoryAdmin)