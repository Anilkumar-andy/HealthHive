from django.shortcuts import render
from .models import Carousel
# Create your views here.
def homepage(request):
    user=request.session.get('username')
    img_c=Carousel.objects.all()
    total = range(img_c.count())
    context={
        'img_c':img_c,
        'total':total,
        'user':user,                     
    }
    return render(request,'base.html',context)

def important_links(request):
    return render(request,'home/links.html')