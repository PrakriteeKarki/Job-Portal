
from django.urls import path
from .views import (JobApplicantView,MyJobView,JobCreateView,DeleteJobView,EditJobView,MyApplicationView,
                    HomeView,JobSearchView,JobDetailView,ApplyJobView,LogOutView,CreateJobApiView)
urlpatterns = [
     path('home/', HomeView.as_view(), name='home'),
     path("jobs/search/",JobSearchView.as_view(),name="job-search"),
     path("job/<uuid:pk>/",JobDetailView.as_view(),name="job-detail"),
     path("job/<uuid:pk>/apply/", ApplyJobView.as_view(), name="apply_job"),
     path("jobs/create/",JobCreateView.as_view(),name="create_advert"),
     path("logout/",LogOutView.as_view(),name="logout"),
     path("myjobs/",MyJobView.as_view(),name="myjobs"),
     path("job/<uuid:id>/edit/",EditJobView.as_view(),name="edit-job"),
     path("job/<uuid:id>/delete/",DeleteJobView.as_view(),name="delete-job"),
     path("job/<uuid:job_id>/applicants/",JobApplicantView.as_view(),name="job-applicants"),
     path("api/create/job/",CreateJobApiView.as_view(),name="create_advert_api"),
    path("myapplications/",MyApplicationView.as_view(),name = "my-applications")






]  
