from django.urls import path
from .views import *

urlpatterns=[
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('add-slot/', slot, name='slot'),
    path('add-event/', event, name='event'),
    path('add-ticket/', ticket, name='ticket'),
    path('events/<int:id>/', eventDetail, name='event_details'),
    path('ticket/<int:id>/', ticketDetail, name='ticket_details'),
    path('host/dashboard/', host_dash, name='host_dash'),
    path('host/events/', host_events, name='host_events'),
    path('host/events/<int:id>/', host_event_edit, name='host_event_edit'),
    path('host/events/<int:id>/', host_event_delete, name='host_event_delete'),




]

