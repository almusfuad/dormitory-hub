from django.contrib import admin
from . import models
from django.utils import timezone

# Register your models here.

class BookingAdmin(admin.ModelAdmin):
      list_display = ('student', 'dormitory', 'date_of_booking', 'date_of_checkin', 'date_of_checkout', 'status')
      list_filter = ('status',)
      readonly_fields = ('date_of_checkin', 'date_of_checkout')
      search_fields = ('student__user__email', 'dormitory__name')

      def save_model(self, request, obj, form, change):
            if 'status' in form.changed_data and request.user.is_staff:
                  status = form.cleaned_data.get('status')

                  if status == 'checkedin' and not obj.date_of_checkin:
                        obj.date_of_checkin = timezone.now().date()
                  elif status == 'checkedout' and not obj.date_of_checkout:
                        obj.date_of_checkout = timezone.now().date()

            super().save_model(request, obj, form, change)

admin.site.register(models.Booking, BookingAdmin)
