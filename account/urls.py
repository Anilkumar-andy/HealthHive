from django.urls import path
from . import views

urlpatterns = [ 
    path('Trainer_registration/', views.register,name='register_trainer'),
    path('user_registration/', views.register_platformUser,name='register_platform_user'),
    path('TrainerData_registration/<str:username>/', views.registerTrainerData,name='register_trainerData'),
    path('PlatformUserData_registration/<str:username>/', views.platformUserData,name='register_PlatformUserData'),
]
