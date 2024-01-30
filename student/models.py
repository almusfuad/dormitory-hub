from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
      user = models.OneToOneField(User, on_delete = models.CASCADE)
      image = models.ImageField(upload_to = 'student/media/images/')
      # gender = models.CharField(max_length=5, blank=True, choices=[('M', 'Male'),('F', 'Female')])
      phone_no = models.CharField(max_length = 15)
      account_no = models.CharField(max_length = 8, unique=True)
      balance = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
      slug = models.CharField(max_length = 100, unique = True)
   
      def __str__(self):
            return f'{self.phone_no} - {self.user.first_name}'
      
      
