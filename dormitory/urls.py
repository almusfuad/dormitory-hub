from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'dormitory'

dormitory_router = DefaultRouter()
dormitory_router.register('list', views.DormitoryViewSet, basename='dormitory')

review_router = DefaultRouter()
review_router.register('all', views.ReviewListViewSet, basename='review')

urlpatterns = [
      path('dormitories/',include(dormitory_router.urls)),
      path('dormitories/search/', views.SearchDormitory.as_view(), name='dormitory_search'),
      path('reviews/', include(review_router.urls)),
      path('dormitories/<int:dormitory_id>/reviews/create/', views.ReviewCreateAPIView.as_view(), name = 'review_create'),
      path('reviews/permission/<int:dormitory_id>/', views.CreateReviewPermissionAPIView.as_view(), name = 'create_permission'),     
]