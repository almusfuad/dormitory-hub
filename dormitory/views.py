from django.shortcuts import render, get_object_or_404
from rest_framework import views, viewsets, response, generics, mixins, status, filters, authentication, permissions, pagination
from . import models
from . import serializers
from booking.models import Booking
from django.db.models import Q
# from .permissions import IsReviewOwner, IsStayed
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.authentication import TokenAuthentication

class CustomPagination(pagination.PageNumberPagination):
      page_size = 12
      page_size_query_param = 'page_size'
      max_page_size = 1000

class LocationListView(generics.ListAPIView):
      def get(self, request, format = None):
            pagination_class = CustomPagination
            locations = models.Location.objects.all()
            serializer = serializers.LocationSerializer(locations, many = True)
            return response.Response(serializer.data)
      
class DormitoryViewSet(viewsets.ModelViewSet):
      queryset = models.Dormitory.objects.all()
      serializer_class = serializers.DormitoryListSerializer
      pagination_class = CustomPagination
      
      def get_queryset(self):
            queryset = super().get_queryset()
            slug = self.request.query_params.get('slug')

            if slug:
                  try:
                        dormitory = queryset.get(slug=slug)
                        queryset = models.Dormitory.objects.filter(pk=dormitory.pk)
                  except models.Dormitory.DoesNotExist:
                        return response.Response({'error': 'Dormitory not found.'})

            return queryset
      
class SearchDormitory(generics.ListAPIView):
      queryset = models.Dormitory.objects.all()
      serializer_class = serializers.DormitoryListSerializer
      pagination_class = CustomPagination
      filter_backends = [filters.SearchFilter]
      search_fields = ['name', 'facilities', 'location__location']
     
     

# Section for reviews with permissions, create, update and list     
class CreateReviewPermissionAPIView(views.APIView):
      authentication_classes = [authentication.TokenAuthentication]
      permission_classes = [permissions.IsAuthenticated]
      
      def get(self, request, *args, **kwargs):
            dormitory_id = kwargs.get('dormitory_id')
            print(dormitory_id)
            
            # Ensure that the dormitory_slug is provided
            if not dormitory_id:
                  return Response({"has_permission": False, "detail": "Dormitory not found"}, status=400)
            
            
            user = request.user
            user_bookings = Booking.objects.filter(student__user = user, dormitory_id = dormitory_id)
            
            if user_bookings.exists():
                  first_booking = user_bookings.first()
                  
                  if first_booking.status in ['checkedin', 'checkedout']:
                        existing_reviews_count = first_booking.dormitory.review_set.filter(reviewer=user).count()
                        if existing_reviews_count == 0:
                              return response.Response({"has_permission": True}, status = status.HTTP_200_OK)
                        else:
                              return response.Response({"has_permission": False, "detail": "Can edit"})
                  else:
                        return response.Response({"has_permission": False, "detail": "User has not checked in to this dormitory"})
            else:
                  return response.Response({"has_permission": False, "detail": "User has not booked this dormitory"})
            

class ReviewCreateAPIView(generics.CreateAPIView):
      authentication_classes = [authentication.TokenAuthentication]
      permission_classes = [permissions.IsAuthenticated]
      serializer_class = serializers.ReviewSerializer
      
      def create(self, request, *args, **kwargs):
            dormitory_id= self.kwargs.get('dormitory_id')
            print(dormitory_id)
            
            reviewer = self.request.user
            print(reviewer)
            
            request.data['dormitory'] = dormitory_id
            request.data['reviewer'] = reviewer.id
            
            return super().create(request, *args, **kwargs)


class ReviewListViewSet(viewsets.ReadOnlyModelViewSet):
      serializer_class = serializers.ReviewSerializer
      
      
      def get_queryset(self):
            queryset = models.Review.objects.all()
            dormitory_slug  = self.request.query_params.get('dormitory_slug')
            if dormitory_slug:
                  dormitory = get_object_or_404(models.Dormitory, slug = dormitory_slug)
                  queryset = queryset.filter(dormitory_id = dormitory.id)
                  
            return queryset