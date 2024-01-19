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
      
# codes for update the information after successfully logged in    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class BasicInformationSerializer(serializers.ModelSerializer):
      user = UserSerializer()

      class Meta:
            model = models.BasicInformation
            fields = '__all__'
            
      account_no = serializers.CharField(read_only=True)
      balance = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)

      def create(self, validated_data):
            user_data = validated_data.pop('user', {})
            institution_type_data = validated_data.pop('institution_type', None)
            institution_name_data = validated_data.pop('institution_name', None)
            institution_address_data = validated_data.pop('institution_address', None)

            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_instance = user_serializer.save()

            basic_info = BasicInformation.objects.create(user=user_instance, **validated_data)

            # Create the institution information instance if data is provided
            if institution_type_data and institution_name_data and institution_address_data:
                  basic_info.institution_type = institution_type_data
                  basic_info.institution_name = institution_name_data
                  basic_info.institution_address = institution_address_data
                  basic_info.save()

            return basic_info

            def update(self, instance, validated_data):
                  user_data = validated_data.pop('user', {})
                  institution_type_data = validated_data.pop('institution_type', None)
                  institution_name_data = validated_data.pop('institution_name', None)
                  institution_address_data = validated_data.pop('institution_address', None)

            # Update the user instance
            user_instance = instance.user
            user_serializer = UserSerializer(user_instance, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

            # Update the basic information instance
            instance.__dict__.update(validated_data)
            instance.save()

            # Update or create institution information
            if institution_type_data and institution_name_data and institution_address_data:
                  instance.institution_type = institution_type_data
                  instance.institution_name = institution_name_data
                  instance.institution_address = institution_address_data
                  instance.save()

            return instance


class UserAllSerializer(serializers.ModelSerializer):
      basicinformation = BasicInformationSerializer()
      class Meta:
            model = User
            fields = ['username', 'email', 'first_name', 'last_name', 'basicinformation']