from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class EmployerRequiredMixin(LoginRequiredMixin):

    def  dispatch(self, request, *args, **kwargs):

        if request.user.user_type != "EMPLOYER":
            raise PermissionDenied
        
        return super().dispatch(request, *args, **kwargs)