
# For api view  
from rest_framework.views import APIView
from rest_framework.decorators import api_view
# For getting response
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from django.urls import reverse
from django.contrib import messages
# for template view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import StudentSerializer, RegistrationSerializer, LoginSerializer
from django.contrib.auth.models import User
from . import models
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
    def post(self, request, *args, **kwargs):
        registration_serializer = RegistrationSerializer(data=request.data)
        if registration_serializer.is_valid():
            user = registration_serializer.save()

            # Token generation
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Construct activation URL
            confirm_link = self.request.build_absolute_uri(reverse('student:activate', kwargs={'uidb64': uid, 'token': token}))

            # Send activation email
            email_subject = 'Confirm Email'
            email_body = render_to_string('emails/confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, email_body, to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            try:
                email.send()
            except Exception as e:
                # Handle email sending failure
                user.delete()  # Rollback user creation if email sending fails
                messages.error(request, f"Failed to send confirmation email: {str(e)}")
                return Response({'error': 'Failed to send confirmation email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # create student instance
            student_data = {
                'user': user.pk,
                'image': request.data.get('image'),
                'phone_no': request.data.get('phone_no'),
                'account_no': 10000 + user.pk,
                'slug': slugify(user.username),
            }
            student_serializer = StudentSerializer(data=student_data)
            if student_serializer.is_valid():
                student_serializer.save()
                messages.success(request, "Registration successful. Please check your email for confirmation.")
                return Response({'message': 'Registration successful. Please check your email for confirmation.'}, status=status.HTTP_201_CREATED)
            else:
                user.delete()  # This will delete the user if the student instance is not created yet
                errors = student_serializer.errors
                messages.error(request, f"Registration failed: {errors}")
                return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = registration_serializer.errors
            messages.error(request, f"Registration failed. Please correct the errors below.{errors}")
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return JsonResponse({"message": "Your account has been activated"})
    else:
        return JsonResponse({"error": "Invalid activation link or user does not exist."})
 
  
class LoginApiView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    token, _ = Token.objects.get_or_create(user=user)
                    messages.success(request, "Login successful.")
                    return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
                else:
                    messages.error(request, 'Your account is not active.')
                    return Response({'error': 'Your account is not active.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                messages.error(request, "Invalid username or password.")
                return Response({'error': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            messages.error(request, 'Invalid form submission.')
            return Response({'error': 'Invalid form submission.'}, status=status.HTTP_400_BAD_REQUEST)

    
def logout_view(request):
    if request.method == 'GET':
        logout(request)
        messages.warning(request, "You have been logged out.")
        return Response({'message': 'You have been logged out.'}, status=status.HTTP_200_OK)
    
    
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return models.Student.objects.filter(user = self.request.user)
        else:
            return models.Student.objects.none()