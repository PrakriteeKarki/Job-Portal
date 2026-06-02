from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import payment_success,payment_failure,confirm_payment



urlpatterns = [
    # eSewa payment callback — must match your SUCCESS_URL path
     path(
        "application/<uuid:id>/pay/",
        confirm_payment,
        name="esewa-payment"
    ),

    path("success/", payment_success, name="payment-success"),
    path("failure/", payment_failure, name="payment-failure"),
]