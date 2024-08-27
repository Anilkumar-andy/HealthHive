from django.shortcuts import render,get_object_or_404
from .models import Video
from account.models import PlatformUser
from account.models import Trainer
from .forms import Video_form,Image_form,VideoReview_form,CustomPlans_form
from django.views import View
from django.contrib.auth.decorators import login_required
from account.mixins import PlatformUserRequiredMixin,TrainerRequiredMixin
# Create your views here.

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
        return render(request,'data/add.html',{'form':form})
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

class Customplans:
    pass