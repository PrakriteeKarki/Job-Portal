from django import forms 
from .models import JobApplication,JobAdvert


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication
        fields = [
            "name",
            "email",
            "portfolio_url",
            "cv"
        ]
        widgets = {
            "portfolio_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://yourportfolio.com"
            })}




class JobAdvertForm(forms.ModelForm):
    
    class Meta:
        model = JobAdvert
        exclude = [
            "created_by",
            "is_published",
            "application_fee",
        ]
        
        widgets = {
            "deadline": forms.DateInput(attrs={
                "type":"date"
            })
        }


