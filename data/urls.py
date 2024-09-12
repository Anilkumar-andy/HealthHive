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
    path('view_image/',View_Data_Image.as_view(),name='view_image_'),
    path('view_detail_video/<int:video_id>/',View_Detail_Video.as_view(),name='view_detail_video_'),
    path('save_data/image/<int:image_id>/',save_data,name='save_data_image_'),
    path('save_data/video/<int:video_id>/',save_data,name='save_data_video_'),
    path('view_save_data/',saved_data_view,name='view_save_data_'),
    path('delete_saved_data/img/<int:image_id>/',delete_saved_data,name='delete_saved_data_image_'),
    path('delete_saved_data/video/<int:video_id>/', delete_saved_data, name='delete_saved_data_video_'),
]
