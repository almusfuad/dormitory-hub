from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

urlpatterns = [
      path('register/', views.UserRegistrationView.as_view(), name = 'user-registration'),
      path('activate/<uid64>/<token>/', views.activate, name = 'activate'),
]