from django.db import models
from student.models import Student
from dormitory.models import Dormitory
from transaction.models import Transaction
# Create your models here.

class Booking(models.Model):
      student = models.ForeignKey(Student, on_delete=models.CASCADE, name='student')
      dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE, name='dormitory')
      date_of_booking = models.DateField(auto_now_add=True)
      date_of_checkin = models.DateField(null=True, default=None)
      date_of_checkout = models.DateField(null=True, default=None)
      number_of_days = models.IntegerField(default=0)
      number_of_months = models.IntegerField(default=0, )
      number_of_seats = models.IntegerField(default=0)
      total_cost = models.IntegerField(default=0)
      status = models.CharField(choices=[('booked', 'Booked'), ('checkedin', 'Checked In'), ('checkedout', 'Checked Out')], max_length=20, default='booked')
      
      def save(self, *args, **kwargs):
            # calculation for number of days
            if self.number_of_days > 0 and self.number_of_seats > 0:
                  self.total_cost = (
                        self.number_of_days * 
                        self.number_of_seats * 
                        self.dormitory.cost_per_night
                  )
            # calculation for number of months
            elif self.number_of_seats > 0 and self.number_of_months > 0:
                  self.total_cost = (
                        self.number_of_seats * 
                        self.number_of_months * 
                        self.dormitory.cost_per_month
                  )
            super().save(*args, **kwargs)
                  
      
      class Meta:
            ordering = ['date_of_booking']
      
      def __str__(self):
            return f"{self.student} {self.dormitory} {self.date_of_booking} {self.date_of_checkin} {self.number_of_seats} {self.total_cost} {self.status}"