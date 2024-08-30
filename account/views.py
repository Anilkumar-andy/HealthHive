from django.shortcuts import render,redirect,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import *
from .models import Trainer,PlatformUser
from django.views import View
from django.contrib import messages 
from django.contrib.auth import authenticate,login,logout




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
        form = TrainerDataForm()
        return render(request,'account/TrainerDataRegistration.html',{'form':form})
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
        return render(request,'account/PLatformUserDataForm.html',{'form':form})
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
        username = request.POST.get('username')
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
            return render(request, 'account/success.html')
        
def logout_user(request):
    user = request.session.get('username')
    messages.success(request,f'logout Successful, bye bye {user}')
    logout(request)
    return redirect('/')
    
        