from django.shortcuts import render
from django.views import View
# Create your views here.



# class HomeView(View):

#     def get(self,request):
        
#         if not user.is_authenticated:
#             return render(request,"home_guest.html")
#         if request.user.user_type == "jobseeker":
#             return jobseeker_home(request)
#         elif request.user.role == "employer":
#             return employer_home(request)
#          return render(request, "home_guest.html")
