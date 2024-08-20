from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Trainer)
admin.site.register(Slots)
admin.site.register(TrainerData)
admin.site.register(Goals)
admin.site.register(PlatformUser)
admin.site.register(PlatformUserData)