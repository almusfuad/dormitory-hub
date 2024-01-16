from django.db import models

# Create your models here.
class Location(models.Model):
      location = models.CharField(max_length=20)
      slug = models.SlugField(max_length = 30, unique=True)
      
      def __str__(self):
            return self.location
      
class Dormitory(models.Model):
      name = models.CharField(max_length = 50)
      location = models.ForeignKey(Location, on_delete=models.CASCADE, name='location')
      address = models.CharField(max_length=100)
      image = models.ImageField(upload_to = 'dormitory/media/images')
      dormitory_type = models.CharField(choices=[('girls', 'Girls'), ('boys', 'Boys')], max_length=10)
      facilities = models.CharField(choices=[('super', 'Super'), ('regular', 'Regular')], max_length=20)
      cost_per_night = models.IntegerField(default=0, blank=True)
      cost_per_month = models.IntegerField(default=0, blank=True)
      available_seats = models.IntegerField(default=0, blank=True)
      slug = models.SlugField(max_length = 60, unique=True)
      
      def __str__(self):
            return f"{self.name} {self.location.location}"