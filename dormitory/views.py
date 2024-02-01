from django.shortcuts import render
from rest_framework import views, viewsets, response, generics, mixins, status, filters
from . import models
from . import serializers
# from .permissions import IsReviewOwner, IsStayed
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

# rendering home
# def home(request):
#       return render(request, 'dormitory/home.html')

class LocationListView(views.APIView):
      def get(self, request, format = None):
            locations = models.Location.objects.all()
            serializer = serializers.LocationSerializer(locations, many = True)
            return response.Response(serializer.data)
      
class DormitoryViewSet(viewsets.ModelViewSet):
      queryset = models.Dormitory.objects.all()
      serializer_class = serializers.DormitoryListSerializer
      filter_backends = [filters.SearchFilter]
      search_fields = ['name', 'type', 'facilities', 'location__location', 'slug']
      
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
      