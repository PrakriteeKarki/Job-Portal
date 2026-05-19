

from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class' : 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class' : 'form-control',
    })
    )
    class Meta:
        model = Account
        fields = ['user_type', 'email', 'first_name', 'last_name', 'phone_number', 'password']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        placeholders = {
            'user_type':'Enter User Type',
            'email': 'Enter Email Address',
            'first_name': 'Enter First Name',
            'last_name': 'Enter Last Name',
            'phone_number': 'Enter Phone Number',
        }

        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['placeholder'] = placeholder

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("This email already exists.")
        return email 