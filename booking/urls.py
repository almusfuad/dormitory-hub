from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
      path('create/', views.BookingCreateView.as_view(), name = 'booking-create'),
      path('permission/<slug:dormitory_slug>/', views.BookingPermission.as_view(), name = 'booking-permission'),
      path('list/', views.BookingListView.as_view(), name = 'booking-list'),
]