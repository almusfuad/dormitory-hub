from rest_framework import serializers
from . import models
from transaction.models import Transaction
from student.models import BasicInformation
from django.shortcuts import get_object_or_404


class BookingSerializer(serializers.ModelSerializer):
      class Meta:
            model = models.Booking
            exclude = ['date_of_booking', 'date_of_checkin', 'date_of_checkout']
            read_only_fields = ['status', 'total_cost', 'slug']
            
      def create(self, validated_data):
            # create instance for the model booking

            # Create instance for the model booking
            instance = super().create(validated_data)
            
            self.validate_available_seats(instance)
            self.calculate_total_cost(instance)
            self.create_transaction(instance)
            
            return instance
      
      def validate_available_seats(self, instance):
            # check for available seats
            if instance.number_of_seats > instance.dormitory.available_seats:
                  raise serializers.ValidationError('Insufficient seats.')
      
      def calculate_total_cost(self, instance):
            # calculation for number of days
            if instance.number_of_days > 0 and instance.number_of_seats > 0:
                  instance.total_cost = (
                        instance.number_of_days * 
                        instance.number_of_seats * 
                        instance.dormitory.cost_per_night
                  )
            # calculation for number of months
            elif instance.number_of_seats > 0 and instance.number_of_months > 0:
                  instance.total_cost = (
                        instance.number_of_seats * 
                        instance.number_of_months * 
                        instance.dormitory.cost_per_month
                  )
                  
            # check for student balance
            if instance.total_cost > instance.student.balance:
                  raise serializers.ValidationError('Insufficient balance.')
            
            # checking available seats
            if instance.number_of_seats > instance.dormitory.available_seats:
                  raise serializers.ValidationError("Insufficient available seats.")
            
            instance.student.balance -= instance.total_cost
            instance.dormitory.available_seats -= instance.number_of_seats
            instance.student.save()
            instance.dormitory.save()
      
      def create_transaction(self, instance):
            account_no = instance.student.account_no
            basic_information_instance = get_object_or_404(BasicInformation, account_no=account_no)
            # auto generated transaction fields
            transaction = Transaction.objects.create(
                  account=basic_information_instance,
                  amount = instance.total_cost,
                  transaction_type='booking',
                  balance_after_transaction = instance.student.balance,     
            )
            return transaction