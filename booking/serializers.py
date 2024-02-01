from rest_framework import serializers
from django.shortcuts import get_object_or_404
from transaction.models import Transaction
from student.models import Student
from . import models

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        exclude = ['date_of_booking', 'date_of_checkin', 'date_of_checkout']
        read_only_fields = ['status', 'total_cost', 'slug']

    def create(self, validated_data):
        self.validate_available_seats(validated_data)
        self.calculate_total_cost(validated_data)
        transaction = self.create_transaction(validated_data)
        return super().create(validated_data)

    def validate_available_seats(self, validated_data):
        instance = models.Booking(**validated_data)
        if instance.number_of_seats > instance.dormitory.available_seats:
            raise serializers.ValidationError('Insufficient seats.')

    def calculate_total_cost(self, validated_data):
        instance = models.Booking(**validated_data)
        if instance.number_of_days > 0 and instance.number_of_seats > 0:
            total_cost = (
                instance.number_of_days * 
                instance.number_of_seats * 
                instance.dormitory.cost_per_night
            )
        elif instance.number_of_seats > 0 and instance.number_of_months > 0:
            total_cost = (
                instance.number_of_seats * 
                instance.number_of_months * 
                instance.dormitory.cost_per_month
            )
        else:
            total_cost = 0

        student = instance.student
        if total_cost > student.balance:
            raise serializers.ValidationError('Insufficient balance.')

        dormitory = instance.dormitory
        if instance.number_of_seats > dormitory.available_seats:
            raise serializers.ValidationError("Insufficient available seats.")

        student.balance -= total_cost
        dormitory.available_seats -= instance.number_of_seats
        student.save()
        dormitory.save()
        validated_data['total_cost'] = total_cost

    def create_transaction(self, validated_data):
        student = validated_data['student']
        transaction = Transaction.objects.create(
            account=student,
            amount=validated_data['total_cost'],
            transaction_type='booking',
            balance_after_transaction=student.balance,
        )
        return transaction
