from rest_framework.permissions import BasePermission

class IsEmployer(BasePermission):
        
    message = "Only employers can create job advertisements."

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.user_type=="EMPLOYER")