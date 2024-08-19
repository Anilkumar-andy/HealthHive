from django.urls import path
from . import views

urlpatterns = [ 
    path('Trainer_registration/', views.register,name='register_trainer'),
    path('TrainerData_registration/<str:username>/', views.registerTrainerData,name='register_trainerData'),
]
