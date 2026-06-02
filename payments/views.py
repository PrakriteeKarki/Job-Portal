from django.shortcuts import render
import base64
import json
import uuid
from django_esewa import EsewaPayment
from django.views import View
from django.shortcuts import redirect
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404
from django.views import View
from django_esewa import EsewaPayment

from .models import JobApplication
from django_esewa import generate_signature
from django_esewa import EsewaPayment
import hmac
import hashlib
import base64



import uuid
import hmac
import hashlib
import base64
from django.views import View
from django.shortcuts import get_object_or_404, render

import logging

logger = logging.getLogger(__name__)




def confirm_payment(request,id):
    application = get_object_or_404(JobApplication,id=id)
    
    amount = f"{application.job_advert.application_fee:.2f}" 
    transaction_uuid = str(uuid.uuid4())
    secret_key = "8gBm/:&EnhH.1/q"
    payment = EsewaPayment(
        product_code="EPAYTEST",
        success_url="http://localhost:8000/success/",
        failure_url="http://localhost:8000/failure/",
        amount=amount,
        tax_amount="0.00",
        total_amount=amount,
        product_delivery_charge="0.00",
        product_service_charge="0.00",
        transaction_uuid=transaction_uuid,
        secret_key=secret_key,

    )
    signature = payment.create_signature() #Saves the signature as well as return it
    print(signature)

    context = {
        'form':payment.generate_form()
    }
    
    return render(request,'payments/esewa_payment.html',context)
#class EsewaPaymentView(View):

    # def create_signature(self, total_amount, transaction_uuid, product_code):
    #     secret_key = "8gBm/:&EnhH.1/q"

    #     message = "total_amount={},transaction_uuid={},product_code={}".format(
    #         total_amount.strip(),
    #         transaction_uuid.strip(),
    #         product_code.strip()
    #     )

    #     print("SIGNATURE STRING:", message)

    #     digest = hmac.new(
    #         secret_key.encode(),
    #         message.encode(),
    #         hashlib.sha256
    #     ).digest()

    #     return base64.b64encode(digest).decode()

    # def get(self, request, application_id):

    #     application = get_object_or_404(JobApplication, id=application_id)

    #     amount = "{:.2f}".format(float(application.job_advert.application_fee))
    #     transaction_uuid = str(uuid.uuid4())
    #     product_code = "EPAYTEST"

    #     signature = self.create_signature(amount, transaction_uuid, product_code)

    #     print("AMOUNT:", amount)
    #     print("UUID:", transaction_uuid)
    #     print("SIGNATURE:", signature)

    #     form_data = {
    #         "amount": amount,
    #         "tax_amount": "0",
    #         "total_amount": amount,
    #         "transaction_uuid": transaction_uuid,
    #         "product_code": product_code,
    #         "success_url": "http://127.0.0.1:8000/payment/success/",
    #         "failure_url": "http://127.0.0.1:8000/payment/failure/",
    #         "product_service_charge": "0",
    #         "product_delivery_charge": "0",
    #         "signed_field_names": "total_amount,transaction_uuid,product_code",
    #         "signature": signature,
    #     }

    #     return render(request, "payments/esewa_payment.html", {
    #         "form": form_data,
    #         "application": application,
    #     })
    
        
from django.http import HttpResponse
from .models import JobApplication

def payment_success(request):

    transaction_uuid = request.GET.get("transaction_uuid")
    total_amount = request.GET.get("total_amount")

    try:
        application = JobApplication.objects.get(
            id=transaction_uuid
        )

        application.payment_status = "PAID"
        application.paid_amount = total_amount

        application.save()

        return HttpResponse("Payment Successful")

    except JobApplication.DoesNotExist:
        return HttpResponse("Application not found")
    
def payment_failure(request):
    return HttpResponse("Payment Failed")