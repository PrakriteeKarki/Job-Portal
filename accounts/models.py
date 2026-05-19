from django.db import models
from django.contrib.auth.models import BaseUserManager,PermissionsMixin,AbstractBaseUser
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self,user_type,email,first_name,last_name,phone_number,password=None):
        if not user_type:
            raise ValueError("User must have a user type")
        if not email:
            raise ValueError("User must have an email address")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not phone_number:
            raise ValueError("User must have a phone number")

        user=self.model(
            user_type=user_type,    
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        


    def create_superuser(self,email,first_name,last_name,phone_number="0000000000",password=None,user_type='employer'):
        user = self.create_user(
        user_type=user_type,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        password=password,
        )    
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser,PermissionsMixin):

    USER_TYPE_CHOICES=(
        ('jobseeker','Job Seeker'),
        ('employer','Employer'),    
    )
    user_type = models.CharField(max_length=20,choices=USER_TYPE_CHOICES,default='jobseeker')
    email = models.EmailField(unique=True,max_length=100)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['first_name','last_name']
    
    

    objects = MyAccountManager()

    def __str__(self):
        return self.email