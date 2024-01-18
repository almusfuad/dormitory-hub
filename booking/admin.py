from django.contrib import admin
from . import models
from django.utils import timezone
from . views import send_booking_status_email

# Register your models here.



class BookingAdmin(admin.ModelAdmin):
      list_display = ('student', 'dormitory', 'date_of_booking', 'date_of_checkin', 'date_of_checkout', 'status')
      list_filter = ('status',)
      readonly_fields = ('date_of_checkin', 'date_of_checkout')
      search_fields = ('student__user__email', 'dormitory__name')

      def save_model(self, request, obj, form, change):
            if 'status' in form.changed_data and request.user.is_staff:
                  old_status = obj.status
                  new_status = form.cleaned_data.get('status')

                  if new_status == 'checkedin' and not obj.date_of_checkin:
                        obj.date_of_checkin = timezone.now().date()
                        send_booking_status_email(obj.student.user, new_status, "Booking Status Update", 'booking_status_email_template.html')
                  elif new_status == 'checkedout' and not obj.date_of_checkout:
                        obj.date_of_checkout = timezone.now().date()
                        send_booking_status_email(obj.student.user, new_status, "Booking Status Update", 'booking_status_email_template.html')

            super().save_model(request, obj, form, change)

admin.site.register(models.Booking, BookingAdmin)
