from django.shortcuts import render
from rest_framework import generics, permissions, response, status
from django.shortcuts import get_object_or_404
# Create your views here.


from . import models
from . import serializers

class BookingCreateView(generics.CreateAPIView):
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
                  'student': user.basicinformation.pk,
                  'dormitory': dormitory_id,
                  'status': 'booked',
                  'number_of_days': number_of_days,
                  'number_of_months': number_of_months,
                  'number_of_seats': number_of_seats,
            }
            
            serializer = self.get_serializer(data = {**request.data, **booking_data})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            headers = self.get_success_headers(serializer.data)
            return response.Response(serializer.data, status = status.HTTP_201_CREATED, headers=headers)

class BookingListCreateView(generics.ListCreateAPIView):
      queryset = models.Booking.objects.all()
      serializer_class = serializers.BookingSerializer
      permission_classes = [permissions.IsAuthenticated]

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
      queryset = models.Booking.objects.all()
      serializer_class = serializers.BookingSerializer
      permission_classes = [permissions.IsAuthenticated]