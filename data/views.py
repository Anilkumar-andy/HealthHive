from django.shortcuts import render,get_object_or_404,redirect
from .models import Video,Image,SavedData,VideoReview
from account.models import PlatformUser
from account.models import Trainer
from .forms import Video_form,Image_form,VideoReview_form,CustomPlans_form
from django.views import View
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from account.mixins import PlatformUserRequiredMixin,TrainerRequiredMixin
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

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
            return redirect('/')



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
            return redirect('/')
        
        


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



def search_data(request):
    search_term=request.POST.get('search_data')
    print(search_term)
    
    videos_title=Video.objects.filter(
        Q(title__icontains=search_term) |
        Q(category__goals_provided__icontains=search_term) | 
        Q(description__icontains=search_term)
        )
    images_title=Image.objects.filter(
        Q(title__icontains=search_term) |
        Q(category__goals_provided__icontains=search_term) | 
        Q(description__icontains=search_term)
        )
        
    data={
        'videos':videos_title,
        'images':images_title
    }
    return data
        
class View_Data_Video(View):
    def get(self,request):
        videos=Video.objects.all()
        data={
            'videos':videos
        }
        return render (request,'data/all_data.html',{'data':data})
    def post(self,request):
        data=search_data(request)
        return render(request,'data/all_data.html',{'data':data})
        
class View_Data_Image(View):
    def get(self,request):
        images=Image.objects.all()
        data={
            'images':images
        }
        return render (request,'data/all_data.html',{'data':data})
    def post(self,request):
        data=search_data(request)
        return render(request,'data/all_data.html',{'data':data})
    

        
        
def filter_data_goals(request,goal):
    print(goal)
    filter= get_object_or_404(Video,category=goal)
    return render (request,'data/data.html',{'data':filter})
    
@login_required
@csrf_exempt
def save_data(request,image_id=None,video_id = None):
    if request.method == 'POST':
        data=request.POST
        print(data)
        user_instance = request.session.get('username')
        print(user_instance)
        user=get_object_or_404(PlatformUser,user__username = user_instance)
        
        if image_id is not None:
            print("============>",image_id)
            image = get_object_or_404(Image,id=image_id)
            video = None
            print("================>",image)
        if video_id is not None:
            print("============>",video_id)
            video = get_object_or_404(Video,id=video_id)
            image = None
            print("================>",video)
        media, created = SavedData.objects.get_or_create(user=user,image=image,video=video)
        if created:
            message = messages.success(request, 'Data saved successfully')
        if not created:
            message = messages.error(request, 'Data already exists')
        print("=============>",media)
        return redirect('/',{'message':message})
        
@login_required
def delete_saved_data(request,image_id=None,video_id = None):
    if request.method == 'POST':
        data=request.POST
        print("=============>",data)
        
        if image_id is not None:
            print("============>",image_id)
            image = get_object_or_404(Image,id=image_id)
            video = None
            print("================>",image)
        if video_id is not None:
            print("============>",video_id)
            video = get_object_or_404(Video,id=video_id)
            image = None
            print("================>",video)
        data = SavedData.objects.filter(image=image,video=video)
        data.delete()
        return redirect('view_save_data_')
    
@login_required
def saved_data_view(request):
    user_instance = request.session.get('username')
    user=get_object_or_404(PlatformUser,user__username = user_instance)
    data = SavedData.objects.filter(user=user)
    print('=================>',user)
    print('==================>  ',data)
    return render(request,'data/saved_data.html',{'data':data})
    


class Video_review(PlatformUserRequiredMixin,View):
    def get(self,request,video_id):
        form=VideoReview_form()
        
        video_review = VideoReview.objects.filter(video__id = video_id)
        print('=================>data from video review',video_review)

        return render(request,'data/review.html',{'form':form,'video_review':video_review})
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
        
@login_required
def trainer_profile_posts(request,trainer_id):
        trainer = get_object_or_404(Trainer,id=trainer_id)
        videos = Video.objects.filter(user=trainer)
        print("==============>",videos)
        images = Image.objects.filter(user=trainer)    
        print("==============>",images)
        data={
        'videos':videos,
        'images':images,     
    }
        return render(request,'data/all_data.html',{'data':data})

        
