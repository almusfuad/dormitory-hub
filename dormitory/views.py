from django.shortcuts import render
from rest_framework import views, viewsets, response, generics
from . import models
from . import serializers
from .permissions import IsReviewOwner, IsStayed

# Create your views here.
class LocationListView(views.APIView):
      def get(self, request, format = None):
            locations = models.Location.objects.all()
            serializer = serializers.LocationSerializer(locations, many = True)
            return response.Response(serializer.data)
      
class DormitoryListView(views.APIView):
      def get(self, request, format=None):
            location_slug = self.request.query_params.get('location')
            dormitory_type = self.request.query_params.get('type')
            facilities = self.request.query_params.get('facilities')

            # get all the dormitory list
            dormitories = models.Dormitory.objects.all()

            if location_slug:
                  try:
                        location = models.Location.objects.get(slug=location_slug)
                        dormitories = dormitories.filter(location=location)
                  except models.Location.DoesNotExist:
                        return response.Response({'error': 'Location not found.'})

            if dormitory_type:
                  dormitories = dormitories.filter(dormitory_type=dormitory_type)

            if facilities:
                  dormitories = dormitories.filter(facilities=facilities)

            serializer = serializers.DormitoryListSerializer(dormitories, many=True)

            return response.Response(serializer.data)
      
class DormitoryDetailsView(views.APIView):
      def get(self, request, slug, format = None):
            dormitory = models.Dormitory.objects.get(slug = slug)
            serializer = serializers.DormitoryDetailsSerializer(dormitory)
            return response.Response(serializer.data)
      
      
class ReviewListCreateView(generics.ListCreateAPIView):
      queryset = models.Review.objects.all()
      serializer_class = serializers.ReviewSerializer
      # permission_classes = [IsStayed]
      
class ReviewRUDView(generics.RetrieveDestroyAPIView):
      queryset = models.Review.objects.all()
      serializer_class = serializers.ReviewSerializer
      permission_classes = [IsReviewOwner]