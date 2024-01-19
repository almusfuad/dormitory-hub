from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from . import models
from . import serializers
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout

# sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.
class UserRegistrationView(APIView):
      serializer_class = serializers.UserRegistrationSerializer
      
      def post(self, request):
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                  user = serializer.save()
                  
                  token = default_token_generator.make_token(user)
                  uid = urlsafe_base64_encode(force_bytes(user.pk))
                  confirm_link = f"https://dormitory-hub.onrender.com/user/activate/{uid}/{token}"
                  email_subject = 'Confirm email'
                  email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
                  
                  email = EmailMultiAlternatives(email_subject, '', to=[user.email])
                  email.attach_alternative(email_body, 'text/html')
                  email.send()
                  
                  return Response("Check your email for confirmation")
            return Response(serializer.errors)
      

def activate(request, uid64, token):
      try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User._default_manager.get(pk=uid)
      except User.DoesNotExist:
            user = None

      if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login')
      else:
            return HttpResponse("Invalid activation link or user does not exist.", status=400)
      
      
  
class UserLoginView(APIView):
      def post(self, request):
            serializer = serializers.UserLoginSerializer(data = self.request.data)
            if serializer.is_valid():
                  username = serializer.validated_data['username']
                  password = serializer.validated_data['password']
                  
                  user = authenticate(username = username, password = password)
                  
                  if user:
                        token, _ = Token.objects.get_or_create(user = user)
                        print(token)
                        print(_)
                        login(request, user)
                        return Response({'token': token.key, 'user_id': user.id})
                  else:
                        return Response({'error': 'Invalid credentials.'})
            return Response(serializer.errors)   

class UserLogoutView(APIView):
      def get(self, request):
            request.user.auth_token.delete()
            logout(request)
            # return Response({'message': 'Logout successful.'})
            return redirect('login')

class BasicInformationViewSet(viewsets.ModelViewSet):
      queryset = models.BasicInformation.objects.all()
      serializer_class = serializers.BasicInformationSerializer

      def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)

      @action(detail=True, methods=['get'])
      def get_info(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

      def update(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

      def perform_update(self, serializer):
            serializer.save()

      def perform_create(self, serializer):
            serializer.save(user=self.request.user)
                  
            
class UserAllAPIView(APIView):
      def get(self, request, *args, **kwargs):
            try:
                  # Retrieve the User object
                  user_id = kwargs.get('id')
                  user = User.objects.get(pk=user_id)

                  serializer = serializers.UserAllSerializer(user)

                  return Response(serializer.data, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                  return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                  return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)