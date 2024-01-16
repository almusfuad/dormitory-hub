from django.db import models
from student.models import BasicInformation

# Create your models here.
class Transaction(models.Model):
      account = models.ForeignKey(BasicInformation, related_name='account', on_delete=models.CASCADE)
      amount = models.DecimalField(decimal_places=2, max_digits=10)
      transaction_type = models.CharField(choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw'), ('booking', 'Booking')], max_length=10)
      balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=10, default=0)
      timestamp = models.DateTimeField(auto_now_add=True, editable=False)
      
      class Meta:
            ordering = ['timestamp']
            
      def __str__(self):
            return f"{self.account.account_no} - {self.transaction_type} - {self.amount}"