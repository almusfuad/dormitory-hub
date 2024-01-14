from django.db import models
from hotel import models as hotel_models

# Create your models here.
class BedType(models.Model):
      name = models.CharField(max_length=30)
      slug = models.SlugField(max_length=40, unique=True)
      
      def __str__(self):
            return self.name
      
class Features(models.Model):
      name = models.CharField(max_length=20)
      slug = models.SlugField(max_length=40, unique=True)
      
      def __str__(self):
            return self.name

class RoomFacilities(models.Model):
      name = models.CharField(max_length=30)
      slug = models.SlugField(max_length=40, unique=True)
      
      def __str__(self):
            return self.name
      
class Room(models.Model):
      hotel = models.ForeignKey(hotel_models.Hotel, on_delete=models.CASCADE, related_name='rooms')
      bed_type = models.ForeignKey(BedType, on_delete=models.CASCADE, related_name='rooms')
      features = models.ForeignKey(Features, on_delete=models.CASCADE, related_name='rooms')
      room_facilities = models.ManyToManyField(RoomFacilities, related_name='rooms')
      price = models.IntegerField()
      available_room = models.IntegerField()
      
      def __str__(self):
            return f"{self.hotel.name}: {self.bed_type.name}"