from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class StudentSerializer(serializers.ModelSerializer):
      class Meta:
            model = models.StudentInformation
            fields = '__all__'