from django.urls import path
from .views import *

urlpatterns=[
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('add-slot/', slot, name='slot'),
    path('add-event/', event, name='event'),
    path('add-ticket/', ticket, name='ticket'),
    path('events/<int:id>/', eventDetail, name='event_details'),

]