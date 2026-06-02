from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from rest_framework.views import APIView
from django.views.generic import ListView
from rest_framework.response import Response
from .models import JobAdvert
from core.serializers import JobAdvertSerializer,CreateJobSerializer
from django.views.generic import DetailView
from .forms import JobAdvertForm,JobApplicationForm
from .mixins import EmployerRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, generics
from .permissions import IsEmployer
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
# Create your views here.

import logging

logger = logging.getLogger(__name__)

@method_decorator(never_cache, name='dispatch')
class HomeView(ListView):
    model = JobAdvert
    template_name = "core/home.html"
    context_object_name = "job_adverts"
    paginate_by = 4
    ordering = ['-created_at']

    def get_queryset(self):
       
       keyword = self.request.GET.get("keyword")
       location = self.request.GET.get("location")

       queryset = JobAdvert.objects.search(
          keyword=keyword,
          location=location,
       )
       return queryset


#job search function 
class JobSearchAPIView(APIView):

    def get(self,request):

        keyword = request.GET.get('keyword')
        location = request.GET.get('location')
        
        # search is a searching function in models.py
        jobs = JobAdvert.objects.search(keyword,location)
        serializer = JobAdvertSerializer(jobs,many=True)
        return Response(serializer.data)

class JobSearchView(View):

    def get(self, request):

        keyword = request.GET.get('keyword')
        location = request.GET.get('location')

       
        if keyword or location:
          jobs = JobAdvert.objects.search(keyword, location)
        else:
          jobs = JobAdvert.objects.all()

        paginator = Paginator(jobs,10)
        requested_page = request.GET.get('page')
        paginated_adverts = paginator.get_page(requested_page)

        

        return render(
            request,
            'core/home.html',
            {'job_adverts': paginated_adverts,}
        )

class JobDetailView(DetailView):
   model = JobAdvert
   template_name = "core/job_detail.html"
   context_object_name = "job"


class ApplyJobView(View):
   
   def get(self,request,pk):
      
      job = get_object_or_404(JobAdvert,pk=pk)
      form = JobApplicationForm()
      context = {
         "job":job,
         "form":form,
      }
      return render(request,"core/apply_job.html",context)
    
   def post(self,request,pk):
      
      job = get_object_or_404(JobAdvert,pk=pk)
      form = JobApplicationForm(
         request.POST,
         request.FILES
         )
      
      if form.is_valid():
         application = form.save(commit=False)
         application.job_advert = job 
         application.applicant = request.user
         # application.payment_status = "PENDING"
         application.save()
         return render(request,"core/application_success.html")
       
         # #generate esewa payload
         # if application.id:
         #    return redirect("esewa-payment", id=str(application.id))
         # else:
         #    print("ERROR: application.id is empty")
         # # return redirect(
         # #        "esewa-payment",
         # #        application_id=application.id
         # #    )

     
      context = {
         "job" : job,
         "form" : form,
      }
      return render (
         request,
         "core/apply_job.html",
         context
      )

      
      

class JobCreateView(EmployerRequiredMixin,CreateView):
   model = JobAdvert
   form_class = JobAdvertForm 
   template_name = "core/create_job.html"
   success_url = reverse_lazy('home')

   def form_valid(self,form):
      form.instance.created_by = self.request.user
      return super().form_valid(form)

   
class LogOutView(View):
   def get(self,request):
      logout(request)
      return redirect('home')
   
   
class MyJobView(LoginRequiredMixin,View):

   def get(self,request):

      jobs = JobAdvert.objects.filter(created_by=request.user)
      context = {
         "my_jobs":jobs,
      }
      return render(
         request,
         "core/my_jobs.html",
         context
      )
   
class EditJobView(LoginRequiredMixin,View):

   def get(self,request,id):
      job=get_object_or_404(JobAdvert,id=id,created_by=request.user)
      form = JobAdvertForm(instance=job)
      context = {
         "form":form,
         "job":job,
      }
      return render(
         request,
         "core/edit_job.html",
         context
      )
   
   def post(self,request,id):

      job = get_object_or_404(JobAdvert,id=id,created_by=request.user)
      form = JobAdvertForm(
         request.POST,instance=job
      )

      if form.is_valid():
         form.save()
         return redirect("myjobs")
      context = {
         "form":form,
         "job":job
      }
      return  render(
            request,
            "core/edit_job.html",
            context
        )


class DeleteJobView(LoginRequiredMixin,View):

   def post(self,request,id):

      job = get_object_or_404(JobAdvert,id=id,created_by=request.user)
      job.delete()
      messages.success(request, "Job deleted successfully.")
      return redirect("myjobs")
      
class JobApplicantView(LoginRequiredMixin,View):

   def get(self,request,job_id):
      applicants = JobApplication.objects.filter(job_advert__id=job_id).select_related('applicant')
      context = {
         "my_applications" : applicants,
      }
      return render(request,"core/my_applications.html",context)
   


class CreateJobApiView(generics.CreateAPIView):
    serializer_class = CreateJobSerializer
    permission_classes = [IsEmployer]

   # def dispatch(self, request, *args, **kwargs):
   #  logger.debug("DISPATCH HIT")
   #  logger.debug(f"USER: {request.user}")  # SAFE
   #  return super().dispatch(request, *args, **kwargs)
   
   # def create(self, request, *args, **kwargs):
   #  print("USER:", request.user)
   #  print("AUTH:", request.auth)
   #  return super().create(request, *args, **kwargs)
  
   
         
      
class MyApplicationView(ListView):

   model = JobApplication
   template_name = 'core/my_applications.html'
   context_object_name = 'my_applications'

   def get_queryset(self):
       return JobApplication.objects.filter(applicant=self.request.user).order_by('-created_at')
       
