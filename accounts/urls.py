
from django.urls import path
from .views import Register ,RegisterApiView,Login,LoginApiView

urlpatterns = [
     path('register/', Register.as_view(), name='register'),
     path('api/register/', RegisterApiView.as_view(), name='register-api'),
     path('login/', Login.as_view(), name='login'),
     path('api/login/', LoginApiView.as_view(), name='login-api'),


]
