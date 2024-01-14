from django.db import models
from student.models import StudentBankAccount
from . import constants
# Create your models here.


class Transaction(models.Model):
      account = models.ForeignKey(StudentBankAccount, related_name='transactions', on_delete=models.CASCADE)
      amount = models.DecimalField(decimal_places=2, max_digits=10)
      balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=10)
      transaction_type = models.CharField(choices=constants.TRANSACTION_TYPE, max_length=20)
      timestamp = models.DateTimeField(auto_now_add=True)
      return_money = models.BooleanField(default=False)
      
      class Meta:
            ordering = ['timestamp']