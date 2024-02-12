from django.shortcuts import render
from rest_framework import generics, permissions, response, status
from django.shortcuts import get_object_or_404
# Create your views here.
from transaction.views import send_transaction_email
from . import models
from . import serializers

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

# email sending
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

def send_booking_status_email(user, status, subject, template):
      # sending auto email to user
      message = render_to_string(template, {
            'user': 'user',
            'status': 'status',
      })
      send_email = EmailMultiAlternatives(subject, '', to = [user.email])
      send_email.attach_alternative(message, "text/html")
      send_email.send()


class BookingCreateView(generics.CreateAPIView):
      authentication_classes = [TokenAuthentication]
      serializer_class = serializers.BookingSerializer
      permission_classes = [permissions.IsAuthenticated]
      
      def create(self, request, *args, **kwargs):
            user = self.request.user
            
            # Ensure that the provided values for number_of_days, number_of_months, and number_of_seats are valid integers
            try:
                  number_of_days = int(request.data.get('number_of_days', 0))
                  number_of_months = int(request.data.get('number_of_months', 0))
                  number_of_seats = int(request.data.get('number_of_seats', 0))
            except ValueError:
                  return response.Response(
                  {'error': 'Invalid values for number_of_days, number_of_months, or number_of_seats.'},
                  status=status.HTTP_400_BAD_REQUEST
                  )

            # Check if the dormitory ID is provided
            dormitory_id = request.data.get('dormitory')
            if not dormitory_id:
                  return response.Response(
                  {'error': 'Dormitory ID is required.'},
                  status=status.HTTP_400_BAD_REQUEST
                  )

            # # Retrieve the existing dormitory instance using get_object_or_404
            # dormitory = get_object_or_404(Dormitory, id=dormitory_id)
            
            booking_data = {
                  'student': user.student.pk,
                  'dormitory': dormitory_id,
                  'status': 'booked',
                  'number_of_days': number_of_days,
                  'number_of_months': number_of_months,
                  'number_of_seats': number_of_seats,
            }
            
            serializer = self.get_serializer(data = {**request.data, **booking_data})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            # booking confirmation email
            booking_subject = "Booking Confirmation"
            booking_template = 'booking_status_email_template.html'
            send_booking_status_email(user, 'booked', booking_subject, booking_template)
            
            headers = self.get_success_headers(serializer.data)
            return response.Response(serializer.data, status = status.HTTP_201_CREATED, headers=headers)

class BookingListCreateView(generics.ListCreateAPIView):
      serializer_class = serializers.BookingSerializer
      permission_classes = [permissions.IsAuthenticated]
      
      def get_queryset(self):
            user = self.request.user
            return models.Booking.objects.filter(student__user = user)

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
      queryset = models.Booking.objects.all()
      serializer_class = serializers.BookingSerializer
      permission_classes = [permissions.IsAuthenticated]
      
      
      def perform_update(self, serializer):
            old_status = self.get_object().status
            new_status = self.request.data.get('status')
            
            # perform the update
            serializer.save()
            
            # checking of status change
            if old_status != new_status:
                  user = self.request.user
                  subject = "Booking Status Update"
                  template = 'booking_status_email_template.html'