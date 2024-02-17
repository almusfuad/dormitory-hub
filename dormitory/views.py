from django.shortcuts import render, get_object_or_404
from rest_framework import views, viewsets, response, generics, mixins, status, filters, authentication, permissions
from .permissions import CanCreateReviewPermission
from . import models
from . import serializers
# from .permissions import IsReviewOwner, IsStayed
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework.authentication import TokenAuthentication

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
      
class CreateReviewPermissionAPIView(views.APIView):
      # authentication_classes = [authentication.TokenAuthentication]
      permission_classes = [CanCreateReviewPermission]
      
      def get(self, request, format=True):
            # Get the dormitory slug from the request data or URL
            dormitory_slug = request.data.get('dormitory_slug') or request.GET.get('dormitory_slug')
            
            # Ensure that the dormitory_slug is provided
            if not dormitory_slug:
                  return Response({"has_permission": False}, status=400)
            
            # check if the user has permission
            permission = CanCreateReviewPermission()
            has_permission = permission.has_permission(request, self)
            
            return Response({"has_permission": has_permission}, status=200)
      
      

class ReviewCreateAPIView(generics.CreateAPIView):
      authentication_classes = [authentication.TokenAuthentication]
      permission_classes = [permissions.IsAuthenticated]
      serializer_class = serializers.ReviewSerializer
      
      def perform_create(self, serializer):
            dormitory_slug = self.kwargs.get('dormitory_slug')
            dormitory = get_object_or_404(models.Dormitory, slug = dormitory__slug)
            
            serializer.save(
                  dormitory = dormitory,
                  reviewer = self.request.user
            )


class ReviewListViewSet(viewsets.ReadOnlyModelViewSet):
      serializer_class = serializers.ReviewSerializer
      
      
      def get_queryset(self):
            queryset = models.Review.objects.all()
            dormitory_slug  = self.request.query_params.get('dormitory_slug')
            if dormitory_slug:
                  queryset = queryset.filter(dormitory__slug = dormitory_slug)
            return queryset