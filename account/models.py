from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import Permission
# Ensure 'is_trainer' permission is correctly set up

# Create your models here.

class Trainer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='trainer_profile')
    profile_image = models.ImageField(upload_to = 'profile_image/',null=True)
    phone_number = models.CharField( max_length=10,null=False,unique=True)
    dob = models.DateField(null=False)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10,choices=[('male','male'),('female','female'),('others','others')])
    created_at = models.DateTimeField(auto_now_add=True)
    certificate = models.FileField(null=False,upload_to="certificate_pdfs/")
    subscription = models.BooleanField(default= False)
    
    class Meta:
        permissions =[
            ('is_trainer','Is trainer')
        ]

    def __str__(self):
        return self.user.username 
    


class Slots(models.Model):
    start_time =models.TimeField(default='00:00:00',null=False)
    end_time = models.TimeField(default = '00:00:00',null=False)
    
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['start_time','end_time'],name='unique_time_slot' )
        ]
        verbose_name = 'Slot'
        # verbose_name_plural = 'Slot'

    def __str__(self):
        return f'{self.start_time}-{self.end_time}'
    

class TrainerData(models.Model):
    trainer = models.OneToOneField(Trainer,on_delete=models.CASCADE)
    pricing = models.DecimalField(decimal_places=2,max_digits=5,null=False,blank=False)
    time_Slots_1 = models.ForeignKey(Slots,related_name='trainer_data_time_slots_1',on_delete=models.CASCADE,blank=False,null=False)
    time_Slots_2 = models.ForeignKey(Slots,related_name='trainer_data_time_slots_2',on_delete=models.CASCADE,blank=False,null=False)
    time_Slots_3 = models.ForeignKey(Slots,related_name='trainer_data_time_slots_3',on_delete=models.CASCADE,blank=True,null=True)
    time_Slots_4 = models.ForeignKey(Slots,related_name='trainer_data_time_slots_4',on_delete=models.CASCADE,blank=True,null=True)
    time_Slots_5 = models.ForeignKey(Slots,related_name='trainer_data_time_slots_5',on_delete=models.CASCADE,blank=True,null=True)
    time_Slots_6 = models.ForeignKey(Slots,related_name='trainer_data_time_slots_6',on_delete=models.CASCADE,blank=True,null=True)
    time_Slots_7 = models.ForeignKey(Slots,related_name='trainer_data_time_slots_7',on_delete=models.CASCADE,blank=True,null=True)
    verification = models.BooleanField(default = False)
    
    def __str__(self):
        return f'{self.trainer.user.first_name} - verification status : {self.verification}'
    



class PlatformUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='platform_user_profile')
    profile_image = models.ImageField(upload_to = 'profile_image/',null=True)
    phone_number = models.CharField( max_length=10,null=False,unique=True)
    dob = models.DateField(null=False)
    age = models.IntegerField(null=False,blank=False)
    gender = models.CharField(max_length=10,choices=[('male','male'),('female','female'),('others','others')])
    created_at = models.DateTimeField(auto_now_add=True)
    subscription = models.BooleanField(default= False)
    
    class Meta:
        permissions =[
            ('is_platform_user','Is platform user')
        ]

    
    def __str__(self):
        return self.user.username
    
    
class Goals(models.Model):
    goals_provided = models.CharField(max_length=80)

    def __str__(self):
        return f'goals : {self.goals_provided}'
    


BODY_TYPE_CHOICES = [
    ('Ectomorph', 'Ectomorph'),
    ('Endomorph', 'Endomorph'),
    ('Mesomorph', 'Mesomorph'),
    ('Pear or triangle', 'Pear or triangle'),
    ('Inverted triangle', 'Inverted triangle'),
    ('Rectangle', 'Rectangle'),
    ('Hourglass', 'Hourglass'),
    ('Oval or apple', 'Oval or apple'),
]

    
BLOOD_PRESSURE_CHOICES = [
    ('Normal', 'LESS THAN 120	and	LESS THAN 80'),
    ('Elevated', '120 - 129	and	LESS THAN 80'),
    ('HIGH BLOOD PRESSURE (HYPERTENSION) STAGE 1', '130 - 139	or	80 - 89'),
    ('HIGH BLOOD PRESSURE (HYPERTENSION) STAGE 2', '140 OR HIGHER	or	90 OR HIGHER'),
    ('HYPERTENSIVE CRISIS (consult your doctor immediately)', 'HIGHER THAN 180	and/or	HIGHER THAN 120'),
]



class PlatformUserData(models.Model):
    platform_user = models.OneToOneField(PlatformUser,on_delete=models.CASCADE)
    goal = models.ForeignKey(Goals,on_delete=models.CASCADE)
    height = models.DecimalField(decimal_places=2,max_digits=4,null=False,blank=False)
    weight = models.DecimalField(decimal_places=2,max_digits=4,null=False,blank=False)
    Body_type = models.CharField(max_length=50, choices=BODY_TYPE_CHOICES, blank=True)
    blood_pressure = models.CharField(max_length=100, choices=BLOOD_PRESSURE_CHOICES, blank=True) 
    BMI = models.DecimalField(decimal_places=2,max_digits=5,null=False,blank=False)    
    
    def __str__(self):
        return f'{self.platform_user.user.first_name} {self.BMI}'
    
    
class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    flat_shop_number = models.CharField(max_length=100)
    building_name = models.CharField(max_length=100)
    area_street = models.CharField(max_length=100)
    near_by = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.title + ' of user ' + self.user.first_name    

