from django.db import models
from django.urls import reverse 
from django.utils import timezone
from django.db.models import Q
# Create your models here.
import uuid
from accounts.models import Account
from .enums import ApplicationStatus,PaymentStatus,EmploymentType,ExperienceLevel,LocationTypeChoice


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True




class JobAdertQuerySet(models.QuerySet):

    def active(self):
        return self.filter(is_published=True,deadline__gte=timezone.now().date())
    
    def search(self,keyword,location):
        query = Q()

        if keyword:
            query &= (
                  Q(title__icontains=keyword)
                | Q(comapany_name__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(skills__icontains=keyword)
            )

            if location:
                query &= Q(location__icontains=location)

            return self.active().filter(query)






class JobAdvert(BaseModel):
    title = models.CharField(max_length=150)
    company_name = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=100,choices=EmploymentType)
    experience_level = models.CharField(max_length=100,choices=ExperienceLevel)
    description = models.TextField()
    job_type = models.CharField(max_length=100,choices=LocationTypeChoice)
    location = models.CharField(max_length=250,null=True,blank=True)
    is_published = models.BooleanField(default=True)
    deadline = models.DateField()
    skills = models.CharField(max_length=400)
    created_by = models.ForeignKey(Account,on_delete=models.CASCADE)
    application_fee = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=5,
        
    )

    objects = JobAdertQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)

    def publish_advert(self) -> None:
        self.is_published = True 
        self.save(update_fields = ["is_published"])

    @property
    def total_applicants(self):
        return self.applications.count()
    
    def get_absolute_url(self):
        return reverse("job_advert",kwargs = {"advert_id":self.id})
    
    
class JobApplication(BaseModel):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    portfolio_url = models.URLField()
    cv = models.FileField()
    status = models.CharField(max_length=30,choices=ApplicationStatus.choices,default=ApplicationStatus.APPLIED)
    job_advert = models.ForeignKey(JobAdvert,related_name="applications",on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20,choices=PaymentStatus.choices,default=PaymentStatus.PENDING)
    paid_amount = models.DecimalField(max_digits=6,decimal=2,
                                      null=True,blank=True)
    applicant = models.ForeignKey(Account,related_name="job_applicants",on_delete=models.CASCADE)
