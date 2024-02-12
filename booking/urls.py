from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
      path('create/', views.BookingCreateView.as_view(), name = 'booking-create'),
      path('list/', views.BookingDetailView.as_view(), name = 'booking-list'),
]