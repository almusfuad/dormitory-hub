from django.urls import path
from . import views

urlpatterns = [
      path('locations/', views.LocationListView.as_view(), name = 'location-list'),
      path('list/', views.DormitoryListView.as_view(), name = 'dormitory-list'),
      path('list/<slug:slug>', views.DormitoryDetailsView.as_view(), name = 'dormitory-details'),
]