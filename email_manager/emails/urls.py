from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscribe_form, name='subscribe_form'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/<str:email>/', views.unsubscribe, name='unsubscribe'),
    path('send-campaign/<int:campaign_id>/', views.send_campaign, name='send_campaign'),
    path('schedule-campaign/<int:campaign_id>/', views.schedule_campaign, name='schedule_campaign'),
]
