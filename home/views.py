from django.shortcuts import render
from .models import Carousel
from data.models import Video,Image
# Create your views here.
def homepage(request):
    user=request.session.get('username')
    img_c=Carousel.objects.all()
    total = range(img_c.count())
    videos_title=Video.objects.all()
    images_title=Image.objects.all()
    data={
        'img_c':img_c,
        'total':total,
        'user':user,
        'videos':videos_title,
        'images':images_title,                  
    }
    return render(request,'base.html',data)#,context=data)

def important_links(request):
    return render(request,'home/links.html')