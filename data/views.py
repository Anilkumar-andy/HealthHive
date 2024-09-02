from django.shortcuts import render,get_object_or_404
from .models import Video
from account.models import PlatformUser
from account.models import Trainer
from .forms import Video_form,Image_form,VideoReview_form,CustomPlans_form
from django.views import View
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from account.mixins import PlatformUserRequiredMixin,TrainerRequiredMixin
from django.db import IntegrityError
# Create your views here.


'''

views for the TRAINER adding data


'''
class Add_video(TrainerRequiredMixin,View):
    def get(self,request):
        form=Video_form()
        return render(request ,'data/add.html',{'form': form})
    def post(self,request):
        username = request.session.get('username')
        print(username)
        user = get_object_or_404(Trainer,user__username = username)
        print(user)
        form = Video_form(request.POST,request.FILES)
        if form.is_valid():
            video_instance = form.save(commit=False)
            video_instance.user = user
            video_instance.save()
            return render(request,'data/success.html')



class Add_image(TrainerRequiredMixin,View):
    def get(self,request):
        form = Image_form()
        return render(request,'data/add.html',{'form':form})
    
    def post(self,request):
        form =Image_form(request.POST,request.FILES)
        username = request.session.get('username')
        print(username)
        user = get_object_or_404(Trainer,user__username = username)
        print(user)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user=user
            form_instance.save()
            return render(request,'data/success.html')
        
        
class Video_review(PlatformUserRequiredMixin,View):
    def get(self,request,video_id):
        form=VideoReview_form()
        return render(request,'data/add_review.html',{'form':form})
    def post(self,request,video_id):
        form=VideoReview_form(request.POST)
        username = request.session.get('username')
        user = get_object_or_404(PlatformUser,user__username = username)
        video =get_object_or_404(Video,id=video_id)
        if form.is_valid():
            form_instance=form.save(commit=False)
            form_instance.user=user
            form_instance.video=video
            form_instance.save()
            return render(request,'data/success.html')

class Custom_plans(TrainerRequiredMixin,View):
    def get(self,request):
        form = CustomPlans_form()
        return render(request,'data/add.html',{'form':form})
    def post(self,request):
        form= CustomPlans_form(request.POST,request.FILES)
        username=request.session.get('username')
        print(f'============>coming from ===={username}')
        if form.is_valid():
            try:
                custom_plans_instance =form.save(commit=False)
                trainer_instance = get_object_or_404(Trainer,user__username = request.session.get('username'))
                custom_plans_instance.trainer=trainer_instance
                custom_plans_instance.save()
                return render(request,'data/success.html')
            except IntegrityError as e:
                # print(e)
                error_message=(
                    f'custom plan for User trainer {form.cleaned_data.get("uploaded_for_user")} of {form.cleaned_data.get("from_date")} to {form.cleaned_data.get("to_date")} already exists. Please choose another date range'
                )
                messages.error(request, error_message)
                return render (request,'data/add_custom_plans.html',{'form':form})
        else:
            messages.error(request,"form is invalid, check the details")
            return render(request,'data/add.html',{'form':form})
        
        
        
        
'''

Views for PLATFORM USER 

'''

class View_Data_Video(PlatformUserRequiredMixin,View):
    def get(self,request):
        data=Video.objects.all()
        return render (request,'data/Video_view.html',{'data':data})
    
class View_Detail_Video(PlatformUserRequiredMixin,View):
    def get(self,request,video_id):
        data=get_object_or_404(Video,id=video_id)
        print(data.id)
        return render(request,'data/video_detail.html',{'data':data})
        