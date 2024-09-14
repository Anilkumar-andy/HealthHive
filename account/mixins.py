from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages 
from django.conf import settings
from urllib.parse import urlencode
from django.urls import reverse


class TrainerRequiredMixin(UserPassesTestMixin):    
    print("===========>mixin of trainer")
    def test_func(self):
        print("===========>test func of mixin")
        return self.request.user.has_perm('account.is_trainer')
    
    def handle_no_permission(self):
        print("===========>handle no permission of mixin from trainer")
        if not self.request.user.is_authenticated:
            messages.error(self.request,"to Access the page you need to login")
            login_url = reverse(settings.LOGIN_URL)
            next_url = self.request.get_full_path() 
            if next_url:
                print("===========>next url" ,next_url)
                redirect_url = f"{login_url}?{urlencode({'next': next_url})}"
                print(redirect_url)
            else:
                print("===========>next url" )
                redirect_url = login_url
            return redirect(redirect_url)  
        else:
            messages.error(self.request,"You don't have permission to access the specified Url")
            return redirect ('/')
    
class PlatformUserRequiredMixin(UserPassesTestMixin):
    print("===========>mixin of platform user")
    def test_func(self) :
        print("===========>test func of mixin from platform user")
        return self.request.user.has_perm('account.is_platform_user')
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(self.request,"to Access the page you need to login")
            login_url = reverse(settings.LOGIN_URL)
            next_url = self.request.get_full_path() 
            if next_url:
                print("===========>next url" ,next_url)
                redirect_url = f"{login_url}?{urlencode({'next': next_url})}"
                print(redirect_url)
            else:
                print("===========>next url" )
                redirect_url = login_url
            return redirect(redirect_url)  
        else:
            messages.error(self.request,"You don't have permission to access the platform specified Url")
            return redirect ('/')
            
