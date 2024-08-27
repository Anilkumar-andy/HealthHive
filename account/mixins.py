from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages 


class PlatformUserRequiredMixin(UserPassesTestMixin):
    def test_func(self) :
        return self.request.user.has_perm('is_platform_user')
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('Login_User_/')
        messages.error(self.request,"You don't have permission to access the platform specified Url")
        return redirect (self.request.META.get('HTTP_REFERER','/'))
            
    
class TrainerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.has_perm('is_trainer')
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('Login_User_/')
        messages.error(self.request,"You don't have permission to access the specified Url")
        return redirect (self.request.META.get('HTTP_REFERER','/'))