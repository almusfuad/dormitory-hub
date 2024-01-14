from django.db import models

# Create your models here.
class Location(models.Model):
      name = models.CharField(max_length = 30)
      slug = models.SlugField(max_length = 40, blank=True, null=True, unique=True)
      
      def __str__(self):
            return self.name

class Facilities(models.Model):
      name = models.CharField(max_length = 20)
      slug = models.SlugField(max_length = 30, blank=True, null=True, unique=True)
      
      def __str__(self):
            return self.name

class Hotel(models.Model):
      name = models.CharField(max_length=40)
      location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='hotels')
      facilities = models.ManyToManyField(Facilities, related_name='hotels')
      address = models.CharField(max_length = 100)
      phone_no = models.IntegerField(unique=True, null=True)
      description = models.TextField()
      image = models.ImageField(upload_to='hotel/media/images')
      slug = models.SlugField(max_length = 50, blank=True, null=True, unique=True)
      
      
      def __str__(self):
            return self.name