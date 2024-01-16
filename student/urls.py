from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
# router = DefaultRouter()

urlpatterns = [
      path('register/', views.UserRegistrationView.as_view(), name = 'register'),
      path('login/', views.UserLoginView.as_view(), name = 'login'),
      path('logout/', views.UserLogoutView.as_view(), name = 'logout'),
      path('profile/', views.BasicInformationView.as_view(), name = 'profile'),
      path('activate/<uid64>/<token>', views.activate, name = 'activate'),
]