from django.contrib import admin
from . import models

# Register your models here.
class BasicInformationAdmin(admin.ModelAdmin):
      readonly_fields = ['account_no', 'balance']

admin.site.register(models.BasicInformation, BasicInformationAdmin)
admin.site.register(models.InstitutionInformation)