from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [ 
    path('add_video/', Add_video.as_view() ,name='add_video_'),
    path('add_image/',Add_image.as_view(),name='add_image_'),
    path('video_review/<int:video_id>/',Video_review.as_view(),name='video_review_'),
    path('custom_plans/',Custom_plans.as_view(),name='custom_plans_'),
    path('view_video/',View_Data_Video.as_view(),name='view_video_'),
    path('view_detail_video/<int:video_id>/',View_Detail_Video.as_view(),name='view_detail_video_'),
]
