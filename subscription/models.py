from django.db import models
from ckeditor.fields import RichTextField
from account.models import Trainer,PlatformUser
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
duration_choices = [
    ('M','Monthly (1 month)'),
    ('Q ','Quarterly (3 months) '),
    ('S','Half-Yearly (6 months)'),
    ('Y','Yearly (12 months)'),
    ('N','No Subscription'),
    
]
class SubscriptionPlanTrainer(models.Model):
    name=models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    duration = models.CharField(choices=duration_choices,max_length=50)
    features = RichTextField()
    def __str__(self):
        return f'{self.name} plan price is {self.price}'
    
class SubscribedTrainer(models.Model):
    subscription_status_choices = [
        ('Active','Active'),
        ('Pending','Pending'),
        ('Expired','Expired'),
    ]
    payment_id = models.CharField(max_length=128, default='0',null=True)
    trainer = models.ForeignKey(Trainer,on_delete=models.DO_NOTHING)
    plan = models.ForeignKey(SubscriptionPlanTrainer,on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    subscription_date = models.DateTimeField(null=True,blank=True)
    termination_date = models.DateTimeField(null=True,blank=True)
    last_update = models.DateTimeField(auto_now=True)
    subscription_status = models.CharField(choices=subscription_status_choices,max_length=50,default='Pending')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trainer','plan','subscription_status','subscription_date'],name='unique_date_subscription_trainer')
        ]
    def __str__(self):
        return f'{self.trainer.user.username} is subscribed to {self.plan.name} plan'
    
class HireTrainer(models.Model):
    hiring_status_choices = [
        ('Not Hired', 'Not Hired'),
        ('Hired', 'Hired'),
        ('Terminated', 'Terminated'),
    ]
    payment_id = models.CharField(max_length=128, default='0',null=True)
    user = models.ForeignKey(PlatformUser,on_delete=models.DO_NOTHING)
    hired_trainer = models.ForeignKey(Trainer,on_delete=models.DO_NOTHING)
    duration = models.CharField(choices=duration_choices,max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    hiring_date = models.DateTimeField(blank=True,null=True)    
    termination_date = models.DateTimeField(null=True,blank=True)
    last_update = models.DateTimeField(auto_now=True)
    hiring_status = models.CharField(max_length=50,default='Not Hired',choices=hiring_status_choices)
    
    def __str__(self):
        return f'user {self.user.user.username} hired {self.hired_trainer.user.username}'


PAYMENT_STATUS_CHOICE = (
    ('pending','pending'),
    ('processing','processing'),
    ('completed','completed')
)
PAYMENT_METHOD_CHOICE = (
    ('card','card'),
    ('COD','COD'),
    ('UPI','UPI'),
    ('Razor Pay','Razor Pay')
)

class PaymentRecord(models.Model):
    payment_id = models.CharField(max_length=128, default='0')
    payment_signature = models.CharField(max_length=128, default='0')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)  
    payment_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    status = models.CharField(choices=PAYMENT_STATUS_CHOICE, max_length=20, default='pending')
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICE)
    
    def __str__(self):
        return f'Payment {self.payment_id} by {self.user.username}'

