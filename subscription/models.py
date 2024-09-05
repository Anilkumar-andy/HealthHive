from django.db import models
from ckeditor.fields import RichTextField
from account.models import Trainer,PlatformUser
from django.contrib.auth.models import User


# Create your models here.
duration_choices = [
    ('M','Monthly (1 month)'),
    ('Q ','Quarterly (3 months) '),
    ('S','Half-Yearly (6 months)'),
    ('Y','Yearly (12 months)'),
    
]
class SubscriptionPlanTrainer(models.Model):
    name=models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2,max_digits=6)
    duration = models.CharField(choices=duration_choices,max_length=50)
    features = RichTextField()
    def __str__(self):
        return f'{self.name} plan price is {self.price}'
    
class SubscribedTrainer(models.Model):
    trainer = models.ForeignKey(Trainer,on_delete=models.DO_NOTHING)
    plan = models.ForeignKey(SubscriptionPlanTrainer,on_delete=models.DO_NOTHING)
    subscription_date = models.DateTimeField(auto_now_add=True)
    termination_date = models.DateTimeField(null=True,blank=True)
    last_update = models.DateTimeField(auto_now=True)
    subscription_status = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.trainer.user.username} is subscribed to {self.plan.name} plan'
    
class HireTrainer(models.Model):
    user = models.ForeignKey(PlatformUser,on_delete=models.DO_NOTHING)
    hired_trainer = models.ForeignKey(Trainer,on_delete=models.DO_NOTHING)
    duration = models.CharField(choices=duration_choices,max_length=50)
    hiring_date = models.DateTimeField(auto_now_add=True)
    termination_date = models.DateTimeField(null=True,blank=True)
    last_update = models.DateTimeField(auto_now=True)
    hiring_status = models.BooleanField(default=False)
    
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
    ('net_banking','net_banking')
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

