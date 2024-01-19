from django.shortcuts import render
from rest_framework import views, viewsets, response, generics, mixins
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
      def get(self, request, *args, **kwargs):
            dormitory_id = kwargs.get('id')
            dormitory = models.Dormitory.objects.get(id=dormitory_id)
            serializer = serializers.DormitoryDetailsSerializer(dormitory)
            return response.Response(serializer.data)
      
class DormitoryReviewListView(generics.ListAPIView):
      serializer_class = serializers.ReviewSerializer
      
      def get_queryset(self):
            dormitory_id = self.kwargs['id']
            return models.Review.objects.filter(dormitory__id=dormitory_id)
      
class DormitoryReviewCreateView(generics.CreateAPIView):
      serializer_class = serializers.ReviewSerializer
      permission_classes = [IsStayed]
      
      def perform_create(self, serializer):
            dormitory_id = self.kwargs.get('id')
            dormitory = models.Dormitory.objects.get(id = dormitory_id)
            user = self.request.user
            serializer.save(reviewer = user, dormitory=dormitory)
            

      
class DormitoryReviewUpdateView(generics.RetrieveUpdateAPIView):
      serializer_class = serializers.ReviewSerializer
      permission_classes = [IsStayed]
      lookup_field = 'id'
      
      def get_queryset(self):
            dormitory_id = self.kwargs['id']
            return models.Review.objects.filter(dormitory__id = dormitory_id)
      
      def perform_update(self, serializer):
            serializer.save(reviewer=self.request.user)
      