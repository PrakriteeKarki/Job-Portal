
from django.db import models 

class UserType(models.TextChoices):
    
        EMPLOYER =   ("EMPLOYER", "Employer")
        JOB_SEEKER = ( "JOB_SEEKER", "Job Seeker") 
    