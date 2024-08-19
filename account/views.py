from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .forms import TrainerRegistrationForm,TrainerDataForm
from .models import Trainer


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
        
        
        
def 