from django.core.management.base import BaseCommand
from emails.models import Campaign, Subscriber
from emails.tasks import send_campaign_email


class Command(BaseCommand):
    help = 'Send a campaign email to all active subscribers'

    def add_arguments(self, parser):
        parser.add_argument('campaign_id', type=int, help='ID of the campaign to send')
        parser.add_argument(
            '--async',
            action='store_true',
            help='Send emails asynchronously using Celery',
        )

    def handle(self, *args, **options):
        campaign_id = options['campaign_id']
        use_async = options['async']
        
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            subscriber_count = Subscriber.objects.filter(is_active=True).count()
            
            self.stdout.write(
                self.style.SUCCESS(f'Campaign: "{campaign.subject}"')
            )
            self.stdout.write(f'Active subscribers: {subscriber_count}')
            
            if use_async:
                # Send using Celery
                task = send_campaign_email.delay(campaign_id)
                self.stdout.write(
                    self.style.SUCCESS(f'Campaign queued for async sending. Task ID: {task.id}')
                )
            else:
                # Send synchronously
                send_campaign_email(campaign_id)
                self.stdout.write(
                    self.style.SUCCESS('Campaign sent successfully!')
                )
                
        except Campaign.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Campaign with ID {campaign_id} not found.')
            )
