from django.contrib import admin
from .models import Video,Image,VideoReview,CustomPlans
# Register your models here.

admin.site.register(Video)
admin.site.register(Image)
admin.site.register(VideoReview)
admin.site.register(CustomPlans)