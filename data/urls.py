from django.urls import path
from .views import *

urlpatterns = [ 
    path('add_video/', Add_video.as_view() ,name='add_video_'),
    path('add_image/',Add_image.as_view(),name='add_image_'),
    path('video_review/<int:video_id>/',Video_review.as_view(),name='video_review_'),
]