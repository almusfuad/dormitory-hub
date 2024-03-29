from rest_framework import serializers
from student.models import Student
from . import models

class BasicInformationSerializer(serializers.ModelSerializer):
      class Meta:
            model = Student
            fields = ['account_no', 'balance']

class DepositSerializer(serializers.ModelSerializer):
      class Meta:
            model = models.Transaction
            fields = ['amount']

      def validate_amount(self, value):
            if value < 100:
                  raise serializers.ValidationError('Minimum deposit amount is 100.')
            if value > 10000:
                  raise serializers.ValidationError('Maximum deposit amount is 10000.')
            return value

      def create(self, validated_data):
            request = self.context.get('request')
            account = request.user.student  # accessing via reverse relationship
            amount = validated_data['amount']

            balance_after_transaction = account.balance + amount

            # update balance
            account.balance += amount
            account.save()

            # create transaction
            transaction = models.Transaction(
                  account=account,
                  amount=amount,
                  transaction_type='deposit',
                  balance_after_transaction=balance_after_transaction,
            )

            transaction.save()

            return transaction

class WithdrawSerializer(serializers.ModelSerializer):
      class Meta:
            model = models.Transaction
            fields = ['amount']

      def validate_amount(self, value):
            if value < 100:
                  raise serializers.ValidationError('Minimum withdrawal amount is 100.')
            if value > 5000:
                  raise serializers.ValidationError('Maximum withdrawal amount is 5000.')
            return value

      def validate(self, data):
            request = self.context.get('request')
            account = request.user.student  # accessing via reverse relationship
            amount = data['amount']

            if amount > account.balance:
                  raise serializers.ValidationError('Insufficient balance.')

            return data

      def create(self, validated_data):
            request = self.context.get('request')
            account = request.user.student  # accessing via reverse relationship
            amount = validated_data['amount']

            balance_after_transaction = account.balance - amount

            # update balance
            account.balance -= amount
            account.save()

            transaction = models.Transaction(
                  account=account,
                  amount=amount,
                  transaction_type='withdraw',
                  balance_after_transaction=balance_after_transaction,
            )
            transaction.save()
            return transaction

class TransactionSerializer(serializers.ModelSerializer):
      class Meta:
            model = models.Transaction
            fields = '__all__'
