from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BasicInformation


class UserSerializer(serializers.ModelSerializer):
      class Meta:
            model = User
            fields = {'username', 'email', 'first_name', 'last_name', 'password'}
            extra_kwargs = {'password': {'write_only': True}}
            
      def create(self, validated_data):
            validated_data['is_active'] = False
            user = User.objects.create_user(**validated_data)
            return user
      
class BasicInformationSerializer(serializers.ModelSerializer):
      user = UserSerializer()
      account_no = serializers.CharField(max_length = 12, read_only = True)
      balance = serializers.DecimalField(max_digits = 10, decimal_places = 2, default = 0, read_only = True)
      
      class Meta:
            model = BasicInformation
            fields = {'user', 'image', 'phone_no'}
            
      def create(self, validated_data):
            user_data = validated_data.pop('user')
            user = User.objects.create_user(**user_data)
            account_no = 1000 + user.id
            basic_info = BasicInformation.objects.create(user = user, account_no=account_no, **validated_data)
            return basic_info
      
      def update(self, instance, validated_data):
            user_data = validated_data.pop('user')
            user = instance.user
            instance.image = validated_data.get('image', instance.image)
            instance.phone_no = validate_data.get('phone_no', instance.phone_no)
            instance.save()
            
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.set_password(user_data.get('password', user.password))
            user.save()
            return instance


