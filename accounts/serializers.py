from rest_framework import serializers
from .models import Account
from django.contrib.auth import authenticate




class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
    write_only=True,
    required=True
)

    class Meta:
        model = Account
        fields = ['user_type','email','first_name','last_name','phone_number','password']
        extra_kwargs = {
            'password' : {
                'write_only' : True
                  }
                  }
    
    def create(self,validated_data):
        password = validated_data.pop('password')
        user = Account(**validated_data)
        user.set_password(password)
        user.save()
        return user
         

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self,data):
        
        email = data.get('email')
        password = data.get('password')
      

        if  email and password:
            user = authenticate(username=email,password=password)


            if not user :
                raise serializers.ValidationError("Invalid credentials")
            
            if not user.is_active:
                raise serializers.ValidationError("User is disabled")
            
            data['user'] = user
            return data
        
        raise serializers.ValidationError("Email and password are required")

            




         
        
       




# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self,data):
#         email = data.get('email')
#         password = data.get('password')

#         if not email or not password:
#             raise serializers.ValidationError("Email and password are required")
 
#         try:
#             user = Account.objects.get(email=email)
#         except Account.DoesNotExist:
#             raise serializers.ValidationError("Invalid Credentials.")
        
#         if not user.check_password(password):
#             raise serializers.ValidationError("Inavalid Credentials.")
          
#         if not user.is_active:
#             raise serializers.ValidationError("Account is disabled.")
        
#         data['user'] = user
#         return data
