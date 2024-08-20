from django import forms
from .models import *


def CreateUser(form):
    username = form.cleaned_data.get('username')
    password=form.cleaned_data.get('password')
    first_name=form.cleaned_data.get('first_name')
    last_name=form.cleaned_data.get('last_name')
    email=form.cleaned_data.get('email')
    return User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
    
    
class TrainerRegistrationForm(forms.ModelForm):
    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=50,widget=forms.PasswordInput)
    first_name=forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)
    email=forms.EmailField()   

    class Meta:
        model = Trainer
        exclude = ['user','subscription','created_at']
        widgets = {
            'dob' :forms.DateInput(attrs={'type':'date'})
        }
        
    field_order = ['username','email','profile_image','first_name','last_name','phone_number','certificate','dob','age','gender',]

    def save(self,commit=True):
        user=CreateUser(self)
        Trainer = super().save(commit=False)
        Trainer.user=user
        Trainer.user.is_active = False
        if commit:
            Trainer.user.save()
            Trainer.save()
        return Trainer


class TrainerDataForm(forms.ModelForm):
    class Meta:
        model = TrainerData
        exclude = ['verification','trainer']
    field_order =['pricing','time_Slots_1','time_Slots_2','time_Slots_3','time_Slots_4','time_Slots_5','time_Slots_6','time_Slots_7']


class PlatformUserDataForm(forms.ModelForm):
    class Meta:
        model = PlatformUserData
        exclude = ['platform_user']
    

class PlatformUserForm(forms.ModelForm):
    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=50,widget=forms.PasswordInput)
    first_name=forms.CharField(max_length=50)
    last_name=forms.CharField(max_length=50)
    email=forms.EmailField()
    
    class Meta:
        model = PlatformUser
        exclude =['user','subscription','created_at','subscription']
        widgets = {
            'dob' :forms.DateInput(attrs={'type':'date'})
        }
    
    def save(self,commit=True):
        user = CreateUser(self)
        PlatformUser = super().save(commit=False)
        PlatformUser.user = user
        if commit:
            PlatformUser.user.save()
            PlatformUser.save()
        return PlatformUser 
    

class PlatformUserDataForm(forms.ModelForm):
    class Meta:
        model = PlatformUserData
        exclude = ['platform_user']
    