from .models import Trainer,PlatformUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


@receiver(post_save,sender=Trainer)
def trainer_permission(sender,instance,created,**kwargs):
    print("===========>signals are working of trainner")
    if created:
        print(f"trainer {instance} created")
        model_refernce=ContentType.objects.get_for_model(Trainer) #getting the refernce for the model
        permission=Permission.objects.get(codename='is_trainer',content_type=model_refernce)
        instance.user.user_permissions.add(permission)
        


@receiver(post_save,sender=PlatformUser)
def trainer_permission(sender,instance,created,**kwargs):
    print("===========>signals are working of platform user")   
    if created:
        print(f"platform user {instance} created")
        model_refernce=ContentType.objects.get_for_model(PlatformUser) #getting the refernce for the model
        permission=Permission.objects.get(codename='is_platform_user',content_type=model_refernce)
        instance.user.user_permissions.add(permission)
