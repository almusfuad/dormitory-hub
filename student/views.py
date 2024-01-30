# from django.shortcuts import render, redirect
# from rest_framework import viewsets, status
# from . import models
# from . import serializers
# from rest_framework.decorators import action
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate, login, logout

# # sending email
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string

# Create your views here.
# class UserRegistrationView(APIView):
#       serializer_class = serializers.UserRegistrationSerializer
      
#       def post(self, request):
#             serializer = self.serializer_class(data = request.data)
#             if serializer.is_valid():
#                   user = serializer.save()
                  
#                   token = default_token_generator.make_token(user)
#                   uid = urlsafe_base64_encode(force_bytes(user.pk))
#                   confirm_link = f"https://dormitory-hub.onrender.com/user/activate/{uid}/{token}"
#                   email_subject = 'Confirm email'
#                   email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
                  
#                   email = EmailMultiAlternatives(email_subject, '', to=[user.email])
#                   email.attach_alternative(email_body, 'text/html')
#                   email.send()
                  
#                   return Response("Check your email for confirmation")
#             return Response(serializer.errors)
      

# def activate(request, uid64, token):
#       try:
#             uid = urlsafe_base64_decode(uid64).decode()
#             user = User._default_manager.get(pk=uid)
#       except User.DoesNotExist:
#             user = None

#       if user is not None and default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             return redirect('https://dormitory-hub-front.vercel.app/auth/login.html')
#       else:
#             return HttpResponse("Invalid activation link or user does not exist.", status=400)
      
      
  
# class UserLoginView(APIView):
#       def post(self, request):
#             serializer = serializers.UserLoginSerializer(data = self.request.data)
#             if serializer.is_valid():
#                   username = serializer.validated_data['username']
#                   password = serializer.validated_data['password']
                  
#                   user = authenticate(username = username, password = password)
                  
#                   if user:
#                         token, _ = Token.objects.get_or_create(user = user)
#                         print(token)
#                         print(_)
#                         login(request, user)
#                         return Response({'token': token.key, 'user_id': user.id})
#                   else:
#                         return Response({'error': 'Invalid credentials.'})
#             return Response(serializer.errors)   

# class UserLogoutView(APIView):
#       def get(self, request):
#             request.user.auth_token.delete()
#             logout(request)
#             # return Response({'message': 'Logout successful.'})
#             return redirect('login')

# class BasicInformationViewSet(viewsets.ModelViewSet):
#       queryset = models.BasicInformation.objects.all()
#       serializer_class = serializers.BasicInformationSerializer

#       def create(self, request, *args, **kwargs):
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=201, headers=headers)

#       @action(detail=True, methods=['get'])
#       def get_info(self, request, *args, **kwargs):
#             instance = self.get_object()
#             serializer = self.get_serializer(instance)
#             return Response(serializer.data)

#       def update(self, request, *args, **kwargs):
#             instance = self.get_object()
#             serializer = self.get_serializer(instance, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             self.perform_update(serializer)
#             return Response(serializer.data)

#       def perform_update(self, serializer):
#             serializer.save()

#       def perform_create(self, serializer):
#             serializer.save(user=self.request.user)
                  
            
# class UserAllAPIView(APIView):
#       def get(self, request, *args, **kwargs):
#             try:
#                   # Retrieve the User object
#                   user_id = kwargs.get('id')
#                   user = User.objects.get(pk=user_id)

#                   serializer = serializers.UserAllSerializer(user)

#                   return Response(serializer.data, status=status.HTTP_200_OK)

#             except User.DoesNotExist:
#                   return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#             except Exception as e:
#                   return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


# For api view  
from rest_framework.views import APIView
from rest_framework.decorators import api_view
# For getting response
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from django.contrib import messages
# for template view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import StudentSerializer, RegistrationSerializer, LoginSerializer
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth import authenticate, login, logout
# for email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# user verification
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.models import Token



# user registration and Active
class RegisterAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'student/register.html'

    def post(self, request, *args, **kwargs):
        registration_serializer = RegistrationSerializer(data=request.data)
        
        if registration_serializer.is_valid():
            user = registration_serializer.save()
            
            # Token generation
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Construct activation URL
            confirm_link = self.request.build_absolute_uri(reverse('student:activate', kwargs = {'uid64': uid, 'token': token}))
            
            # Send activation email
            email_subject = 'Confirm Email'
            email_body = render_to_string('emails/confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, email_body, to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            
            # create student instance
            user_instance = User.objects.get(pk = user.pk)
            print(user_instance)
            student_data = {
                'user': user_instance.pk,
                'image': request.data.get('image'),
                'phone_no': request.data.get('phone_no'),
                'account_no': 10000 + user_instance.id,
                'slug': slugify(user_instance.username),
            }
            print('student data:' , student_data)
            
            student_serializer = StudentSerializer(data = student_data)
            if student_serializer.is_valid():
                student_serializer.save()
                messages.success(request, "Registration successful. Please check your email for confirmation.")
                return HttpResponseRedirect(reverse('student:login'))
            else:
                user.delete()  # This will delete the user if the student instance is not created yet
                errors = student_serializer.errors
                messages.error(request, f"Registration failed: {errors}")
                return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)  
        else:
            errors = registration_serializer.errors
            print(errors)
            messages.error(request, f"Registration failed. Please correct the errors below.{errors}")
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        registration_serializer = RegistrationSerializer()
        return Response({'registration_serializer': registration_serializer})

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully.")
        return HttpResponseRedirect(reverse("student:login"))
    else:
        messages.error(request, "Invalid activation link or user does not exist.")
        return HttpResponseRedirect(reverse('student:register'))
 
  
class LoginApiView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'student/login.html'

    def get(self, request, *args, **kwargs):
        return Response({'serializer': LoginSerializer()})

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            print(username, password)
            user = authenticate(
                request,
                username = username,
                password = password,
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    token, _ = Token.objects.get_or_create(user=user)
                    messages.success(request, "Login successful.")
                    return HttpResponseRedirect(reverse('student:login'))
                else:
                    messages.error(request, 'Your account is not active.')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            print(serializer.errors)
            messages.error(request, 'Invalid form submission.')
        return self.get(request)
    
def logout_view(request):
    if request.method == 'GET':
        logout(request)
        messages.warning(request, "You have been logged out.")
        return HttpResponseRedirect(reverse('student:login'))