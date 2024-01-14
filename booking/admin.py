from django.contrib import admin
from . import models
from transaction.models import Transaction
from django.utils import timezone

# Register your models here.
@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
      list_display = [
            'hotel',
            'booking_person',
            'room',
            'check_in_date',
            'check_out_date',
            'total_price',
            'checkout',
      ]
      
      readonly_fields = [
            # 'check_in_date',
            'check_out_date',
            # 'total_price',
      ]
      
      def save_model(self, request, obj, form, change):
            if obj.checkout:
                  obj.check_out_date = timezone.now()
                  
            super().save_model(request, obj, form, change)
