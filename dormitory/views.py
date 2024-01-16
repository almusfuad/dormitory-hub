from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from . import serializers

# Create your views here.
class LocationListView(APIView):
      def get(self, request, format = None):
            locations = models.Location.objects.all()
            serializer = serializers.LocationSerializer(locations, many = True)
            return Response(serializer.data)
      
class DormitoryListView(APIView):
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
                        return Response({'error': 'Location not found.'})

            if dormitory_type:
                  dormitories = dormitories.filter(dormitory_type=dormitory_type)

            if facilities:
                  dormitories = dormitories.filter(facilities=facilities)

            serializer = serializers.DormitoryListSerializer(dormitories, many=True)

            return Response(serializer.data)
      
class DormitoryDetailsView(APIView):
      def get(self, request, slug, format = None):
            dormitory = models.Dormitory.objects.get(slug = slug)
            serializer = serializers.DormitoryDetailsSerializer(dormitory)
            return Response(serializer.data)