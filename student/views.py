from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User

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
                  confirm_link = f"http://127.0.0.1:8000/activate/{uid}/{token}"
                  email_subject = 'Confirm your email'
                  email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
                  
                  email = EmailMultiAlternatives(email_subject, '', to={user.email})
                  email.attach_alternative(email_body, 'text/html')
                  
                  return Response({'message': 'User registration successful. Check your email for confirmation.'}, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
      

def activate(request, uid64, token):
      try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = user._default_manager.get(pk=uid)
      except(User.DoesNotExist):
            user = None
      
      if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('user-registration')
      else:
            return redirect('user-registration')