from django.contrib import admin
from . import models

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):
      readonly_fields = ['account', 'amount', 'transaction_type', 'balance_after_transaction']

admin.site.register(models.Transaction, TransactionAdmin)
      