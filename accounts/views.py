from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
import logging
from rest_framework.authentication import SessionAuthentication
from .throttles import LoginThrottle
from accounts.serializers import RegisterSerializer,LoginSerializer
from django.views import View
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from .models import Account
from django.urls import reverse
from .forms import RegistrationForm
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
# Create your views here.

import logging
logger=logging.getLogger('__name__')

# class RegisterApiView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegisterApiView(APIView):
    
    def post(self,request):

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    






class Register(View):

    def get(self, request):
        form = RegistrationForm()
        return render(request,'accounts/register.html',{'form':form})
    def post(self, request):

        logger = logging.getLogger(__name__)
        form = RegistrationForm(request.POST)

        try:
            if form.is_valid():

                user_type = form.cleaned_data['user_type']
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']

                user = Account.objects.create_user(
                    user_type=user_type,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    password=password
                )

                user.phone_number = phone_number
                user.save()

                logger.info(f"User registered successfully: {email}")

                messages.success(request,"Check your email for verification.")
                return render(request, 'accounts/email_verification_sent.html')
            else:
                print(form.errors.as_json())
                logger.warning("Form is invalid")
                logger.warning(form.errors)

                return render(request,'accounts/register.html', {
                    'form': form
                })

        except Exception as e:
            logger.exception("Unexpected error during registration")
            messages.error( request,"Something went wrong.")
            return redirect('register')   



        


   
def send_activation_email(request,user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message=render_to_string('accounts/account_verification_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    email = EmailMessage(mail_subject,message,to=[user.email])
    email.send()

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        
        return redirect('login')
    
    return redirect('Invalid_activation.')


class LoginApiView(APIView):

    throttle_classes = [LoginThrottle]

    def post(self,request):
        
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            login(request,user)

            return Response({
                'message' : 'Login successful.',
                'user_id' : user.id,
                'email' : user.email,
            },
            status = status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





# class  LoginApiView(APIView):
    
#     throttle_classes = [LoginThrottle]

#     def post(self,request):
#         print("LOGIN VIEW HIT")
#         print(request.body)
#         serializer = LoginSerializer(data=request.data)

#         if serializer.is_valid():
#             user = serializer.validated_data['user']

#             return Response({
#                 'message':'Login successful.',
#                 'user_id':user.id,
#                 'email':user.email ,

#             },
#             status = status.HTTP_200_OK)
        
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class Login(View):

    logger = logging.getLogger(__name__)

    def get(self,request):
        return render(request,'accounts/login.html')
    
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Email and password are required")
            return render(request, 'accounts/login.html')
        
        
        user = authenticate(request, email=email, password=password)
         
        if user is None:
           messages.error(request, "Invalid credentials")
           return render(request, 'accounts/login.html')
        
        
        if not user.is_active:
            messages.error(request, "Account is not active")
            return render(request, 'accounts/login.html')
        
        login(request, user)

        messages.success(request,"Login Successful.")
        return redirect('home')
    
class LogOutAPIView(APIView):

    def post(self,request):
        pass
