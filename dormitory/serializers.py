from rest_framework import serializers
from . import models

class LocationSerializer(serializers.ModelSerializer):
      class Meta:
            model = models.Location
            fields = '__all__'
            
class DormitoryListSerializer(serializers.ModelSerializer):
      location = LocationSerializer()
      class Meta:
            model = models.Dormitory
            fields = '__all__'
            


class DormitoryDetailsSerializer(serializers.ModelSerializer):
      class Meta:
            model = models.Dormitory
            fields = '__all__'
            
class ReviewSerializer(serializers.ModelSerializer):
      class Meta:
            model = models.Review
            fields = '__all__'