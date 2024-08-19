from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request,'home/home.html')

def important_links(request):
    return render(request,'home/links.html')