from django.db import models
from hotel.models import Hotel
from student.models import StudentInformation
from room.models import Room

# Create your models here.
class Booking(models.Model):
      hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
      booking_person = models.ForeignKey(StudentInformation, on_delete=models.CASCADE, related_name='bookings')
      room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
      check_in_date = models.DateField()
      check_out_date = models.DateField(null=True, blank=True)
      total_price = models.DecimalField(max_digits=10, decimal_places=2)
      checkout = models.BooleanField(default=False)
      
      
      