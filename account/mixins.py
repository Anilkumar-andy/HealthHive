from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages 

class TrainerRequiredMixin(UserPassesTestMixin):    
    print("===========>mixin of trainer")
    def test_func(self):
        print("===========>test func of mixin")
        has_permission_ = self.request.user.has_perm('account.is_trainer')
        print(f"========>permission of {self.request.user} is {has_permission_}")
        return has_permission_
    
    def handle_no_permission(self):
        print("===========>handle no permission of mixin from trainer")
        if not self.request.user.is_authenticated:
            messages.error(self.request,"to Access the page you need to login")
            return redirect('Login_User_/')
        else:
            messages.error(self.request,"You don't have permission to access the specified Url")
            return redirect (self.request.META.get('HTTP_REFERER','/'))
    
class PlatformUserRequiredMixin(UserPassesTestMixin):
    print("===========>mixin of platform user")
    def test_func(self) :
        print("===========>test func of mixin from platform user")
        return self.request.user.has_perm('account.is_platform_user')
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.requset,"to Access the page you need to login")
            return redirect('Login_User_/')
        else:
            messages.error(self.request,"You don't have permission to access the platform specified Url")
            return redirect (self.request.META.get('HTTP_REFERER','/'))
            
    
