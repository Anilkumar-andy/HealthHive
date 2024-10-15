from django.urls import path
from . import views

urlpatterns = [ 
    path('Trainer_registration/', views.register,name='register_trainer'),
    path('user_registration/', views.register_platformUser,name='register_platform_user'),
    path('TrainerData_registration/<str:username>/', views.registerTrainerData,name='register_trainerData'),
    path('PlatformUserData_registration/<str:username>/', views.platformUserData,name='register_PlatformUserData'),
    path('login/',views.Login_User.as_view(),name ='Login_User_'  ),
    path('logout/',views.logout_user,name='logout_user_'),
    path('forgot_password/',views.ForgotPassword.as_view(),name='forgot_password_'),
    path('otp_verification/',views.otp_verifcation,name='otp_verifiaction_'),
    path('reset_password/',views.reset_password,name='reset_password_'),

]
