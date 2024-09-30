from account.models import PlatformUser,Trainer



def user_type(request):
    logged_in_user=request.session.get('username')
    print(f"=======================>{logged_in_user}")
    request.session['is_trainer'] = Trainer.objects.filter(user__username=logged_in_user).exists()
    request.session['is_platform_user'] = PlatformUser.objects.filter(user__username=logged_in_user).exists()
    
    return {
        'session':request.session
    }