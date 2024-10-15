from django.core.mail import send_mail,EmailMessage
from django.shortcuts import render,redirect
from django.conf import settings


def send_predefined_mail(request,to):
    subject = "this email is from django server sending predefined email"
    message = "this is test message from "
    from_email = settings.EMAIL_HOST_USER
    to_ = ["hritika2001naik@gmail.com"]
    # recipient_list = [User.objects.all()[1].email]
    send_mail(subject,message,from_email,recipient_list =[to_])    
    
    return render (request, 'predefined_mail.html',{'message':'send again? click once more'})