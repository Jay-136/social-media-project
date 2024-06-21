from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from .models import CustomUser

@shared_task
def Response(firstname,recievermail):
    subject = "Welcome to Social Media App"
    message = f"Heyy! {firstname}, thank you for registering in Social Media App"
    sendermail = settings.EMAIL_HOST_USER 
    mail = EmailMessage(subject,message,sendermail,[recievermail]) 
    mail.send()   
    
    
@shared_task
def send_mail():
    subject = "Welcome to Social Media App"
    message = f"Heyy!, thank you for registering in Social Media App"
    sendermail = settings.EMAIL_HOST_USER 
    reciever_mail = list(CustomUser.objects.values_list('email',flat=True))
    # for mail_i in reciever_mail :
    mail = EmailMessage(subject,message,sendermail,reciever_mail) 
    mail.send()   