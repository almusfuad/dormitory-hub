from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.
class BasicInformation(models.Model):
      user = models.OneToOneField(User, on_delete = models.CASCADE)
      image = models.ImageField(upload_to = 'student/media/images/')
      phone_no = models.CharField(max_length = 15)
      account_no = models.CharField(max_length = 12, unique=True)
      balance = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)

      
      def __str__(self):
            return f'{self.phone_no} - {self.user.first_name}'
      
      
