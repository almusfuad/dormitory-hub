from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.StudentInformation)
admin.site.register(models.StudentAddress)
admin.site.register(models.StudentInstitution)
admin.site.register(models.StudentBankAccount)