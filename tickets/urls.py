from django.urls import path
from .views import *

urlpatterns=[
    path('', index, name='index'),

    path('site-admin/', site_admin, name='site_admin'),
    path('search/', searchevents, name='search'),

    path('site-admin/events/<int:id>/delete/', site_admin_ticket_delete, name='site_admin_ticket_delete'),
    path('site-admin/rsvp/<int:id>/delete/', site_admin_rsvp_delete, name='site_admin_rsvp_delete'),


    path('add-category/', home, name='home'),
    path('add-slot/', slot, name='slot'),
    path('add-event/', event, name='event'),
    path('add-ticket/', ticket, name='ticket'),
    path('events/<int:id>/', eventDetail, name='event_details'),
    path('ticket/<int:id>/', ticketDetail, name='ticket_details'),
    path('host/dashboard/', host_dash, name='host_dash'),
    path('host/events/', host_events, name='host_events'),

    path('host/sales/', host_sales, name='host_sales'),


    path('host/events/<int:id>/update/', host_event_edit, name='host_event_edit'),
    path('host/events/<int:id>/delete/', host_event_delete, name='host_event_delete'),
    path('host/ticket/<int:id>/', host_ticket_details, name='host_ticket_details'),
    path('host/ticket/<int:id>/update/', admin_ticket_edit, name='admin_ticket_edit'),
    path('host/ticket/<int:id>/delete/', admin_ticket_delete, name='admin_ticket_delete'),
    path('host/sales/<int:id>/delete/', host_sales_delete, name='host_sales_delete'),

    path('access/token/', getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa/', lipa_na_mpesa_online, name='lipa_na_mpesa'),

        # register, confirmation, validation and callback urls
    path('c2b/register/', register_urls, name="register_mpesa_validation"),
    path('c2b/confirmation/', confirmation, name="confirmation"),
    path('c2b/validation/', validation, name="validation"),
    path('c2b/callback/', call_back, name="call_back"),
]

# register_urls