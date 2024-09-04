from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SubscriptionPlanTrainer)
admin.site.register(SubscribedTrainer)
admin.site.register(HireTrainer)
admin.site.register(PaymentRecord)