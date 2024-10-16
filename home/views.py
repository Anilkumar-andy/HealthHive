from django.shortcuts import render
from .models import Carousel
from data.models import Video,Image
from account.models import PlatformUser,Trainer






# Create your views here.
def homepage(request):
    
    
        
    img_c=Carousel.objects.all()
    total = range(img_c.count())
    videos_title=Video.objects.all()
    images_title=Image.objects.all()
    trainer_profile=Trainer.objects.all()
    print(f"======================>trainer profile:{trainer_profile}")
    data={
        'img_c':img_c,
        'total':total,
        # 'user':user,
        'videos':videos_title,
        'images':images_title,     
        'trainer_profile':trainer_profile             
    }
    return render(request,'home/home.html',data)#,context=data)

def important_links(request):
    return render(request,'home/links.html')


