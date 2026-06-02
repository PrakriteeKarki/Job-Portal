from rest_framework import serializers
from .models import JobAdvert,JobApplication


class JobAdvertSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobAdvert
        fields = "__all__"

class JobAppliationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobApplication

        fields = [
            "name",
            "email",
            "portfolio_url",
            'cv',
        ]

        

class CreateJobSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobAdvert
        fields = [
            'title',
            'company_name',
            'employment_type',
            'experience_level',
            'description',
            'job_type',
            'location',
            'deadline',
            'skills',
            'application_fee'
            ]
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user
        return JobAdvert.objects.create(**validated_data)
    
        
        
    # def post(self,request):

    #     if data.is_valid():

    #         job = JobAdvert(**self.validated_data)
    #         job.save()


