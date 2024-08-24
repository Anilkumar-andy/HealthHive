from django.urls import path
from .views import *

urlpatterns = [ 
    path('add_video/', Add_video.as_view() ,name='register_trainer'),
    path('add_image/',Add_image.as_view(),name='add_image'),
]