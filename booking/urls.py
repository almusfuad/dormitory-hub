from django.urls import path
from . import views


urlpatterns = [
      path('', views.BookingCreateView.as_view(), name = 'booking-create'),
      path('list/', views.BookingListCreateView.as_view(), name = 'booking-list'),
]