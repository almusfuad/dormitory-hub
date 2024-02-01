from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

app_name = 'student'

router = DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profile')

urlpatterns = [
      path('', include(router.urls)),
      path('register/', views.RegisterAPIView.as_view(), name = 'register'),
      path('activate/<uid64>/<token>/', views.activate, name = 'activate'),
      path('login/', views.LoginApiView.as_view(), name = 'login'),
      path('logout/', views.logout_view, name = 'logout'),
]