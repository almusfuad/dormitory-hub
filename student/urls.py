from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# router = DefaultRouter()
# router.register('profile', views.BasicInformationViewSet, basename='profile')

# urlpatterns = [
#       path('register/', views.UserRegistrationView.as_view(), name = 'register'),
#       path('login/', views.UserLoginView.as_view(), name = 'login'),
#       path('<int:id>/', views.UserAllAPIView.as_view(), name = 'all'),
#       path('', include(router.urls)),
#       path('logout/', views.UserLogoutView.as_view(), name = 'logout'),
#       path('activate/<uid64>/<token>/', views.activate, name = 'activate'),
# ]
app_name = 'student'

urlpatterns = [
      path('register/', views.RegisterAPIView.as_view(), name = 'register'),
      path('activate/<uid64>/<token>/', views.activate, name = 'activate'),
      path('login/', views.LoginApiView.as_view(), name = 'login'),
      path('logout/', views.logout_view, name = 'logout'),
]