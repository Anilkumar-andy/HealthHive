from django.db import models
from account.models import Trainer,PlatformUser

# Create your models here.
class Video(models.Model):
    user= models.ForeignKey(Trainer,on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/',null=False,blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=25,null=False,blank=False)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title
    
class Image(models.Model):
    user= models.ForeignKey(Trainer,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image_data/',null=False,blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=25,null=False,blank=False)
    description = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.title
    
class VideoReview(models.Model):
    video= models.ForeignKey(Video,on_delete=models.CASCADE)
    user = models.ForeignKey(PlatformUser,on_delete=models.CASCADE)
    review = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.video.title} - {self.review[:20]}'

class CustomPlans(models.Model):
    user = models.ForeignKey(PlatformUser,on_delete=models.CASCADE)
    plan_pdf = models.FileField(upload_to='plans/',null=False,blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    week = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    from_date = models.DateField()
    to_date = models.DateField()
    class meta:
        constraints =[
            models.UniqueConstraint(fields=['from_date','to_date','user'],name='unique_date')
        ]
    
