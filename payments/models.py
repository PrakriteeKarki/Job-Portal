from django.db import models
from core.models import *
from core.enums import PaymentStatus
from accounts.models import Account


class PaymentMethod(models.TextChoices):
    ESEWA = ("ESEWA","esewa")


class Payment(models.Model):

    #who paid
    user = models.ForeignKey(Account,
                             on_delete=models.CASCADE,
                             related_name="payments")
    
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    #which job this payment is for 
    job = models.ForeignKey(JobAdvert,on_delete=models.CASCADE,related_name="payments")

    #payment tracking
    status = models.CharField(max_length=20,choices=PaymentStatus.choices,default=PaymentStatus.PENDING)
    #payment method 
    payment_method = models.CharField(max_length=20,choices=PaymentMethod.choices,default=PaymentMethod.ESEWA)
    #esewa reference id 
    transaction_id = models.CharField(max_length=100,unique=True,null=True,blank=True)
    #esewa response payload 
    response_data = models.JSONField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.job} - {self.status}"