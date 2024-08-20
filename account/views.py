from django.shortcuts import render,redirect,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import TrainerRegistrationForm,TrainerDataForm,PlatformUserForm,PlatformUserDataForm
from .models import Trainer,PlatformUser


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
        
def platformUserData(request,username):
    if request.method == 'GET':
        form = PlatformUserDataForm()
        return render(request,'account/PLatformUserDataForm.html',{'form':form})
    elif request.method == "POST":
        form = PlatformUserDataForm(request.POST)
        if form.is_valid():
            print(form.errors)
            platform_user_instance = get_object_or_404(PlatformUser,user__username=username)
            platform_instance = form.save(commit=False)
            platform_instance.platform_user= platform_user_instance
            platform_instance.save()
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
    if request.method == 'GET':
        form = PlatformUserDataForm()
        return render(request,'account/PLatformUserDataForm.html',{'form':form})
    elif request.method == "POST":
        form = PlatformUserDataForm(request.POST)
        if form.is_valid():
            print(form.errors)
            platform_user_instance = get_object_or_404(PlatformUser,user__username=username)
            platform_instance = form.save(commit=False)
            platform_instance.platform_user= platform_user_instance
            platform_instance.save()
            return render(request,'account/success.html')
        else:
            return HttpResponse('form is not valid')
        
        


        