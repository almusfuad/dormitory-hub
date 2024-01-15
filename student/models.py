from django.db import models
from django.contrib.auth.models import User
from . import constants
# Create your models here.
class StudentInformation(models.Model):
      user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='student')
      birth_date = models.DateField(null = True, blank=True)
      gender = models.CharField(max_length = 10, choices=constants.GENDER_TYPE)
      phone_no = models.IntegerField(unique=True)
      account_no = models.IntegerField(unique=True)
      balance = models.DecimalField(default=0, decimal_places=2, max_digits=10)
      
      def __str__(self):
            return f"{self.account_no}"
      
  
class StudentInstitution(models.Model):
      student = models.ForeignKey(StudentInformation, on_delete=models.CASCADE, related_name='institution')
      institution_name = models.CharField(max_length = 50)
      institution_type = models.CharField(max_length = 10, choices=constants.INSTITUTION_TYPE)
      institution_address = models.CharField(max_length = 100)
      
      def __str__(self):
            return f"{self.institution_name} - {self.institution_type}"
      
      