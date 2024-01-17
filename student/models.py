from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.
class BasicInformation(models.Model):
      user = models.OneToOneField(User, on_delete = models.CASCADE)
      gender_type = models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)
      image = models.ImageField(upload_to = 'student/media/images/')
      phone_no = models.CharField(max_length = 11, unique = True)
      street_address = models.CharField(max_length = 100)
      city = models.CharField(max_length = 30)
      postal_code = models.CharField(max_length = 6)
      account_no = models.CharField(max_length = 11, editable=False)
      balance = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0, editable=True)
      
      def __str__(self):
            return f'{self.phone_no} - {self.user.first_name}'
      
      def save(self, *args, **kwargs):
            if not self.account_no:
                  if len(self.phone_no) != 11:
                        raise ValueError('Phone number must be 11 digits.')
                  remaining_digits = self.phone_no[1:]
                  random_digit = str(random.randint(0, 9))
                  self.account_no = f"{remaining_digits}{random_digit}"
            super().save(*args, **kwargs)


    
class InstitutionInformation(models.Model):
      student = models.OneToOneField(BasicInformation, on_delete = models.CASCADE)
      institution_type = models.CharField(choices=[('school', 'School'), ('college', 'College'), ('university', 'University')],
                              max_length=20)
      institution_name = models.CharField(max_length = 100)
      institution_address = models.CharField(max_length = 100)
      
      def __str__(self):
            return f'{self.student.user.first_name} - {self.student.phone_no} - {self.institution_name}'