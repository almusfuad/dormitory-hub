from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class UserRegistrationSerializer(serializers.ModelSerializer):
      confirm_password = serializers.CharField(required=True)
      class Meta:
            model = User
            fields = ['username', 'email', 'password', 'confirm_password']
      
      def save(self):
            username = self.validated_data['username']
            email = self.validated_data['email']
            password = self.validated_data['password']
            password2 = self.validated_data['confirm_password']
            
            if password != password2:
                  raise serializers.ValidationError({'error': 'Password mismatch.'})
            if User.objects.filter(username=username).exists():
                  raise serializers.ValidationError({'error': 'Username already exists.'})
            if User.objects.filter(email = email).exists():
                  raise serializers.ValidationError({'error': 'Email already exists.'})
            account = User(username=username, email=email)
            account.set_password(password)
            account.is_active = False
            account.save()
            return account
      
class UserLoginSerializer(serializers.Serializer):
      username = serializers.CharField(required=True)
      password = serializers.CharField(required=True)
      
class BasicInformationSerializer(serializers.ModelSerializer):
      class Meta:
            model = models.BasicInformation
            fields = ['first_name', 'last_name', 'gender_type', 'image', 'phone_no', 'street_address', 'city', 'postal_code']
            
      def save(self, **kwargs):
            user = self.instance.user
            first_name = self.validated_data['first_name']
            last_name = self.validated_data['last_name']
            gender_type = self.validated_data['gender_type']
            image = self.validated_data['image']
            phone_no = self.validated_data['phone_no']
            street_address = self.validated_data['street_address']
            city = self.validated_data['city']
            postal_code = self.validated_data['postal_code']
            
            user_info = user.objects.update(
                  first_name = first_name,
                  last_name = last_name,
            )
            
            basic_info = models.BasicInformation.objects.create(
                  user = user,
                  gender_type = gender_type,
                  image = image,
                  phone_no = phone_no,
                  street_address = street_address,
                  city = city,
                  postal_code = postal_code,
            )
            return basic_info