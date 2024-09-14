from django.shortcuts import render

# Create your views here.
def homepage(request):
    user=request.session.get('username')
    return render(request,'base.html',{'user':user})

def important_links(request):
    return render(request,'home/links.html')