from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models
from . import serializers
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

# sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

# Create your views here.
class DepositWithdrawAPIView(APIView):
      authentication_classes = [TokenAuthentication]
      permission_classes = [IsAuthenticated]
      
      def post(self, request, *args, **kwargs):
            serializer = None
            if request.data.get('transaction_type') == 'deposit':
                  serializer = serializers.DepositSerializer(data = request.data, context = {'request': request})
            elif request.data.get('transaction_type') == 'withdraw':
                  serializer = serializers.WithdrawSerializer(data = request.data, context = {'request': request})
            else:
                  return Response({'error': 'Invalid Transaction Type'}, status = status.HTTP_400_BAD_REQUEST)
            
            if serializer.is_valid():
                  transaction = serializer.save()
                  
                  # send transaction email to user
                  user = request.user
                  amount = serializer.validated_data['amount']
                  subject = "Transaction Update"
                  template = "transaction_type_update_email_template.html"
                  send_transaction_email(user, amount, subject, template)
                  
                  return Response({'message': 'Transaction Successful', 'data': serializer.data}, status = status.HTTP_201_CREATED)
            else:
                  return Response({'error': serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
            
            
class TransactionViewset(viewsets.ReadOnlyModelViewSet):
      authentication_classes = [TokenAuthentication]
      permission_classes = [IsAuthenticated]
      serializer_class = serializers.TransactionSerializer
      
      def get_queryset(self):
            user = self.request.user
            return models.Transaction.objects.filter(account__user = user)