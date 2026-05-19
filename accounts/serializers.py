from rest_framework import serializers
from .models import Account
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user_type','email', 'password','first_name','last_name','phone_number']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = Account.objects.create_user(
            user_type=validated_data['user_type'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self,data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required")
 
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Invalid Credentials.")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Inavalid Credentials.")
          
        if not user.is_active:
            raise serializers.ValidationError("Account is disabled.")
        
        data['user'] = user
        return data
