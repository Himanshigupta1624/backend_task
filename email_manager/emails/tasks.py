from celery import shared_task
from celery import group
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import Campaign,Subscriber
from django.template.loader import render_to_string
import traceback
from django.conf import settings

@shared_task
def send_campaign_email(campaign_id):
    campaign=Campaign.objects.get(id=campaign_id)
    subscribers=Subscriber.objects.filter(is_active=True)
    # for subscriber in subscribers:
    #     try:
    #         send_email_to_subscriber(subscriber,campaign)
    #     except Exception as e:
    #         print(f"Failed to send email to {subscriber.email}: {str(e)}") 
    tasks=group(
        send_single_email.s(subscriber.id,campaign_id)
        for subscriber in subscribers
    )
    tasks.apply_async()

@shared_task
def send_single_email(subscriber_id,campaign_id):
    subscriber = Subscriber.objects.get(id=subscriber_id)
    campaign = Campaign.objects.get(id=campaign_id)
    try:
        send_email_to_subscriber(subscriber,campaign)
    except Exception as e:
        print(f"Failed to send email to {subscriber.email}: {str(e)}")        
            

def send_email_to_subscriber(subscriber,campaign):
    
    context={
        'first_name': subscriber.first_name,
        'subject': campaign.subject,
        'preview_text': campaign.preview_text,
        'article_url': campaign.article_url,
        'html_content': campaign.html_content,
        }
    body=render_to_string('email.html',context)
    
    msg=MIMEMultipart()
    msg['From']=settings.DEFAULT_FROM_EMAIL
    msg['To']=subscriber.email
    msg['Subject']=campaign.subject 
    msg.attach(MIMEText(body, 'html'))
    try:
        server=smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()   
        print(f"Email sent successfully to {subscriber.email}")  
    except Exception as e:
        print(f"Failed to send email to {subscriber.email}: {str(e)}")
        traceback.print_exc()
        
        raise
        
                    