from django.contrib import admin
from . import models

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
      readonly_fields = ['account_no', 'balance']

admin.site.register(models.Student, StudentAdmin)