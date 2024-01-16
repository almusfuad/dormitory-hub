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

class InstitutionInformationSerializer(serializers.ModelSerializer):
      class Meta:
            model = models.InstitutionInformation
            fields = ['institution_name', 'institution_type', 'institution_address']

class BasicInformationSerializer(serializers.ModelSerializer):
      user = UserSerializer()
      institution_information = InstitutionInformationSerializer(allow_null=True, required=False)

      class Meta:
            model = models.BasicInformation
            exclude = ['balance']
            
      account_no = serializers.CharField(read_only=True)

      def create(self, validated_data):
            user_data = self.context['request'].user
            institution_information_data = validated_data.pop('institution_information', None)

            # Include the user data in the validated_data
            validated_data['user'] = user_data

            try:
                  # Create the basic information instance
                  basic_info = models.BasicInformation.objects.create(**validated_data)

                  # Create the institution information instance if data is provided
                  if institution_information_data is not None:
                        institution_info = models.InstitutionInformation.objects.create(student=basic_info, **institution_information_data)
                        basic_info.institution_information = institution_info

                  return basic_info

            except IntegrityError as e:
                  # Handle the IntegrityError for the unique constraint on phone_no
                  raise serializers.ValidationError({'phone_no': ['Basic information with this phone no already exists.']})
            
      
      def update(self, instance, validated_data):
            user_data = validated_data.pop('user', {})
            institution_information_data = validated_data.pop('institution_information', None)

            # Update the user instance
            user = instance.user
            user_serializer = UserSerializer(user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

            # Update the basic information instance
            instance.__dict__.update(validated_data)
            instance.save()

            # Update or create institution information
            if institution_information_data is not None:
                  institution_info, created = models.InstitutionInformation.objects.get_or_create(
                  student=instance, defaults=institution_information_data
                  )

            # Include the serialized data for InstitutionInformation and User in the response
            serializer = self.__class__(instance=instance)
            return serializer.data