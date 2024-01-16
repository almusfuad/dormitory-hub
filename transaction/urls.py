from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('all', views.TransactionViewset, basename='transactions')

urlpatterns = [
      path('deposit-withdraw/', views.DepositWithdrawAPIView.as_view(), name = 'deposit_withdraw'),
      path('', include(router.urls)),
]