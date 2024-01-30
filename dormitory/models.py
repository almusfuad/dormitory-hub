from django.db import models
from django.contrib.auth.models import User

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
      cost_per_night = models.DecimalField(default=0, blank=True, decimal_places=2, max_digits=10)
      cost_per_month = models.DecimalField(default=0, decimal_places=2, max_digits=10,  blank=True)
      available_seats = models.IntegerField(default=0, blank=True)
      slug = models.SlugField(max_length = 60, unique=True)
      
      def __str__(self):
            return f"{self.name} {self.location.location}"
      
      
class Review(models.Model):
      RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )
      
      dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE, name = 'dormitory')
      reviewer = models.ForeignKey(User, on_delete=models.CASCADE, name = 'reviewer')
      rating = models.PositiveIntegerField(choices = RATING_CHOICES)
      comment = models.TextField()