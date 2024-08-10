from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Trainer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='trainer_profile')
    profile_image = models.ImageField(upload_to = 'profile_image/',null=True)
    phone_number = models.CharField( max_length=10,null=False,unique=True)
    dob = models.DateField(null=False)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10,choices=[('male','male'),('female','female'),('others','others')])
    subscription = models.BooleanField(default= False)

    def __str__(self):
        return self.user.username 
    


class Slots(models.Model):
    start_time =models.TimeField(default='00:00:00',null=False)
    end_time = models.TimeField(default = '00:00:00',null=False)
    
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['start_time','end_time'],name='unique_time_slot' )
        ]
    def __str__(self):
        return f'{self.start_time}-{self.end_time}'
    

class Trainer_data(models.Model):
    trainer = models.OneToOneField(Trainer,on_delete=models.CASCADE)
    certificate = models.FileField(null=False,upload_to="certificate_pdfs/")
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
    



class Platform_user(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='platform_user_profile')
    profile_image = models.ImageField(upload_to = 'profile_image/',null=True)
    phone_number = models.CharField( max_length=10,null=False,unique=True)
    dob = models.DateField(null=False)
    gender = models.CharField(max_length=10,choices=[('male','male'),('female','female'),('others','others')])
    subscription = models.BooleanField(default= False)

    
    def __str__(self):
        return self.user.username
    
    
class Goals(models.Model):
    goals_provided = models.CharField(max_length=80)

    def __str__(self):
        return f'goals : {self.goals_provided}'
    

class Bodytype(models.Model):
    type = models.CharField(max_length=50)
    def __str__(self):
        return f'body type : {self.type}'
    
class BloodPressure(models.Model):
    category = models.CharField(max_length=50,null=False,blank=False)
    range = models.CharField(max_length=90,null=False,blank=False)
    
    def __str__(self):
        return f'{self.category}:{self.range}'



class Platform_user_data(models.Model):
    user = models.OneToOneField(Platform_user,on_delete=models.CASCADE)
    goal = models.ForeignKey(Goals,on_delete=models.CASCADE)
    height = models.DecimalField(decimal_places=2,max_digits=4,null=False,blank=False)
    weight = models.DecimalField(decimal_places=2,max_digits=4,null=False,blank=False)
    Body_type = models.ForeignKey(Bodytype,on_delete=models.CASCADE)
    blood_pressure = models.ForeignKey(BloodPressure,on_delete=models.CASCADE)
    BMI = models.DecimalField(decimal_places=2,max_digits=5,null=False,blank=False)    
    
    def __str__(self):
        return f'{self.user.first_name} {self.BMI}'
    
    
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

