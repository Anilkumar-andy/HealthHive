from django.shortcuts import render,get_object_or_404
from .models import Video
from account.models import Trainer
from .forms import Video_form,Image_form
from django.views import View

# Create your views here.
class Add_video(View):
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



class Add_image(View):
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
            
