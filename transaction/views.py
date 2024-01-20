from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers

# sending email
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

def send_transaction_email(user, amount, subject, template):
      message = render_to_string(template, {
            'user': 'user',
            'amount': 'amount',
      })
      send_email = EmailMultiAlternatives(subject, '', to = [user.email])
      send_email.attach_alternative(message, "text/html")
      send_email.send()

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
                  
                  # Send transaction email to the user
                  user = request.user
                  amount = request.data.get('amount')
                  subject = 'Transaction Update'
                  template = 'transaction_update_email_template.html'
                  send_transaction_email(user, amount, subject, template)
                  
                  return Response(serializer.data, status = status.HTTP_201_CREATED)
            else:
                  return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            
class TransactionViewset(viewsets.ModelViewSet):
      permission_classes = [IsAuthenticated]
      queryset = models.Transaction.objects.all()
      serializer_class = serializers.TransactionSerializer