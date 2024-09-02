from django.contrib import admin
from .models import Video,Image,VideoReview,CustomPlans
# Register your models here.


class CustomPlansAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'uploaded_at','updated_at')

admin.site.register(Video)
admin.site.register(Image)
admin.site.register(VideoReview)
admin.site.register(CustomPlans,CustomPlansAdmin)