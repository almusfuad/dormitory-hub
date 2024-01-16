from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers


# Create your views here.
class DepositWithdrawAPIView(APIView):
      permission_classes = [IsAuthenticated]
      def post(self, request, *args, **kwargs):
            if request.data.get('transaction_type') == 'deposit':
                  serializer = serializers.DepositSerializer(data = request.data, context = {'request': request})
            elif request.data.get('transaction_type') == 'withdraw':
                  serializer = serializers.WithdrawSerializer(data = request.data, context = {'request': request})
            else:
                  return Response({'error': "Invalid Transaction Type"}, status = status.HTTP_400_BAD_REQUEST)
            
            if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status = status.HTTP_201_CREATED)
            else:
                  return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            
class TransactionViewset(viewsets.ModelViewSet):
      permission_classes = [IsAuthenticated]
      queryset = models.Transaction.objects.all()
      serializer_class = serializers.TransactionSerializer