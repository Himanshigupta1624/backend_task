from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Subscriber, Campaign
from django_celery_beat.models import PeriodicTask,IntervalSchedule
from .tasks import send_campaign_email
import json

def subscribe_form(request):# subscription form
    return render(request, 'subscribe.html')


@csrf_exempt
@require_http_methods(["POST"]) #Subscribe a new user to the email list
def subscribe(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        first_name = data.get('first_name', '')
        
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
        
        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={'first_name': first_name, 'is_active': True}
        )
        
        if created:
            return JsonResponse({'message': 'Subscribed successfully'})
        else:
            if not subscriber.is_active:
                subscriber.is_active = True
                subscriber.save()
                return JsonResponse({'message': 'Resubscribed successfully'})
            else:
                return JsonResponse({'message': 'Already subscribed'})
                
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def unsubscribe(request,email):
    try:
        subscriber=Subscriber.objects.get(email=email)
        subscriber.is_active=False
        subscriber.save()
        return JsonResponse({'message':'Unsubscribed successfully'})
    except Subscriber.DoesNotExist:
        return JsonResponse({'error':'Subscriber not found.'},status=404)


@require_http_methods(["POST"])
def send_campaign(request, campaign_id):
    """Send a campaign immediately using Celery"""
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        # Queue the task
        task = send_campaign_email.delay(campaign_id)
        return JsonResponse({
            'message': f'Campaign "{campaign.subject}" queued for sending',
            'task_id': task.id
        })
    except Campaign.DoesNotExist:
        return JsonResponse({'error': 'Campaign not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def schedule_campaign(request, campaign_id):
    """Schedule a campaign to be sent daily"""
    try:
        campaign = Campaign.objects.get(id=campaign_id)
        schedule_daily_campaign(campaign_id)
        return JsonResponse({
            'message': f'Campaign "{campaign.subject}" scheduled for daily sending'
        })
    except Campaign.DoesNotExist:
        return JsonResponse({'error': 'Campaign not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def schedule_daily_campaign(campaign_id):
    schedule,created=IntervalSchedule.objects.get_or_create(every=1,period=IntervalSchedule.DAYS)
    PeriodicTask.objects.create(
        interval=schedule,
        name=f'Send Daily Campaign {campaign_id}',
        task='emails.tasks.send_campaign_email',
        args=json.dumps([campaign_id])
    )