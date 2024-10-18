from django.shortcuts import render,redirect,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import *
from .models import Trainer,PlatformUser
from django.views import View
from django.contrib import messages 
from subscription.models import SubscribedTrainer
from django.contrib.auth import authenticate,login,logout
from random import randint





# Create your views here.
def register(request):
    if request.method == "GET":
        form = TrainerRegistrationForm()
        return render(request,'account/RegistrationForm.html',{'form':form})    
    elif request.method=="POST":
        form = TrainerRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            current_trainer_instance = form.save()
            current_trainer=current_trainer_instance.user.username
            return redirect('register_trainerData',current_trainer)
        else:
            return render(request,'account/RegistrationForm.html',{'form':form})  
        
def registerTrainerData(request,username):
    print(username)
    if request.method == "GET":
        # trainer_status = get
        form = TrainerDataForm()
        return render(request,'account/RegistrationForm.html',{'form':form})
    elif request.method == "POST": 
        form = TrainerDataForm(request.POST)
        if form.is_valid():
            trainer_user = get_object_or_404(Trainer,user__username = username)
            trainer_instance = form.save(commit=False)
            trainer_instance.trainer = trainer_user
            trainer_instance.save()
            return render(request,'account/success.html')
        else:
            return HttpResponse('form is not valid')
        
        
def register_platformUser(request):
    if request.method == "GET":
        form =  PlatformUserForm()
        return render(request,'account/RegistrationForm.html',{'form':form})
    elif request.method == "POST":
        form = PlatformUserForm(request.POST,request.FILES)
        if form.is_valid():
            user_instance = form.save()
            current_platformUser= user_instance.user.username
            return redirect('register_PlatformUserData',current_platformUser)          
        else :
            return render(request,'account/RegistrationForm.html')

def platformUserData(request,username):
    print(f'username is {username}')
    platform_user_instance = get_object_or_404(PlatformUser,user__username=username)
    print(f'platform_user_instance is {platform_user_instance}')

    if request.method == 'GET':
        form = PlatformUserDataForm()
        return render(request,'account/RegistrationForm.html',{'form':form})
    elif request.method == "POST":
        form = PlatformUserDataForm(request.POST)
        print(form)
        print(f'{form.errors} and {form.is_valid()}') # 
        if form.is_valid():
            print(form.errors)
            platform_user_instance = get_object_or_404(PlatformUser,user__username=username)
            platform_instance = form.save(commit=False)
            platform_instance.platform_user= platform_user_instance
            platform_instance.save()
            return render(request,'account/success.html')
        else:
            return HttpResponse('form is not valid')
        

class Login_User(View):
    def get(self,request):
        form = LoginUser_Form()
        return render(request,'account/Login.html',{'form':form})
    
    def post(self,request):
        form = LoginUser_Form(request.POST)
        print(form)
        username = request.POST.get('username')
        print("========>",username)
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,"Invalid username!, Username doesn't exists.")
            return redirect('/')
        
        user = authenticate(username=username,password=password)
        
        if user is None :
            messages.error(request,"Password is incorrect")
            return render(request,'account/login.html',{'form':form})
        
        else:
            login(request,user)
            request.session['username']=user.username
            messages.success(request,f"{user.username} is logged in, login Successful")
            next_url = request.GET.get('next')  
            if next_url:
                return redirect(next_url) 
            return redirect('/')
        
def logout_user(request):
    user = request.session.get('username')
    messages.success(request,f'logout Successful, bye bye {user}')
    logout(request)
    return redirect('/')
    
        
        
        
################ forgot password ##################
class ForgotPassword(View):
    def get(self, request):
        username = request.GET.get('username')
        user = get_object_or_404(User,username = username )
      
        request.session['username']=user.username
        
        if user.email :
            request.session['email']=user.email
            return render(request,'account/email_verification.html')
        else:
            messages.error(request,"Can't procced with this username provided by you")
            return redirect('Login_User_')
    def post(self,request):
        email=request.session.get('email')
        user_provided_email = request.POST.get('email')
        if user_provided_email == email:
            print("========================>email verified successfull")
            generate_otp(request)
            return render(request,'account/otp_verification_page.html')
        else:
            messages.error(request,"Can't procced with this username provided by you")
            return redirect('Login_User_')




def otp_verifcation(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == request.session.get('otp'):
            return render(request,'account/reset_password.html')
        elif  int(request.session['attempts'])>1 :
            request.session['attempts']=str(int(request.session['attempts'])-1)
            return render(request,'account/verify_otp.html')
        else:
            messages.error(request,"Something Went Wrong")
            return redirect('login')


def reset_password(request):
    username = request.session['username']
    if request.method == 'POST' and username:
        password = request.POST.get('new_password')
        user = get_object_or_404(User,username=username)
        user.set_password(password)
        print(password)
        user.save()
        messages.success(request,"Password Reset Successfully")
        return redirect('Login_User_')
    else:
        messages.error(request, "Invalid OTP")
        return redirect('Login_User_')

def generate_otp(request):
    otp = randint(1000,9999)
    request.session['otp']=str(otp)
    print(otp)
    request.session['attempts']='3'