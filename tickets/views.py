from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from .models import *
from .forms import *

# Create your views here.
def index(request):
    events_list = Event.objects.filter(closed=False).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(events_list, 1)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    
    context = {
        'events':events,
    }
    return render(request, 'tickets/index.html', context)
    
def search(request):

    results = []

    if request.method == "GET":

        query = request.GET.get('search')

        if query == '':

            query = 'None'

        results = Book.objects.filter(Q(book_name__icontains=query) | Q(author_name__icontains=query) | Q(price__icontains=query) )

    return render(request, 'search.html', {'query': query, 'results': results})



def searchevents(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(title__icontains=query) | Q(description__icontains=query)

            results= Event.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'tickets/search.html', context)

        else:
            return render(request, 'tickets/search.html')

    else:
        return render(request, 'tickets/search.html')


def eventDetail(request, id):
    event = get_object_or_404( Event, id=id)
    tickets = Ticket.objects.filter(event=event)
    

    context = {
        'event':event,
        'tickets':tickets
    }
    return render(request, 'tickets/eventDetails.html', context)

def ticketDetail(request, id):
    ticket = get_object_or_404( Ticket, id=id)

    reservations = Reservation.objects.filter(ticket=ticket).count()
    name = PaymentCategories.objects.get(name=ticket.category)

    all_slots = []

    for slot in ticket.event.available_slots.all():
        if slot.category.name == ticket.category:
            slotss = slot.number_of_seats
            all_slots.append(slotss)
    
    form = ReservationForm()
    if request.method == 'POST':  
        form = ReservationForm(request.POST, request.FILES)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.ticket = ticket
            reservation.save()
            return redirect('ticket_details',  id=ticket.id)

    context = {
        'ticket':ticket,
        'form':form,
        'reservations':reservations,
        'all_slots':all_slots
    }
    return render(request, 'tickets/ticketDetails.html', context)
@login_required
def home(request):
    form = PaymentCategoriesForm()
    if request.method == 'POST':  
        form = PaymentCategoriesForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.company = request.user
            category.save()
            return redirect('host_dash')



    context = {
        'form':form,
    }        


    return render(request, 'tickets/events.html', context)
# @login_required
# def slot(request):
#     if request.method == 'POST':
#         form = SlotForm(request.user, request.POST)
#         if form.is_valid():
#             slot = form.save(commit=False)
#             slot.company = request.user
#             slot.save()
#             return redirect('slot')
#     else:
#         form = SlotForm(request.user)
#     return render(request, 'tickets/slot.html', {'form': form})

@login_required
def slot(request): 
    companycat = PaymentCategories.objects.filter(company=request.user)
    # comppany = request.user

    form = SlotForm()
    form.fields['category'].queryset = PaymentCategories.objects.filter(company=request.user)
    if request.method == 'POST':  
        form = SlotForm( request.POST, request.FILES)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.company = request.user
            slot.save()
            return redirect('host_dash')

    context = {
        'form':form,
    }        


    return render(request, 'tickets/events.html', context)

@login_required
def event(request): 

    form = EventForm()
    form.fields['available_slots'].queryset = Slot.objects.filter(company=request.user)
    if request.method == 'POST':  
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.company = request.user
            event.save()
            return redirect('ticket')

    context = {
        'form':form,
    }        


    return render(request, 'tickets/events.html', context)

@login_required
def ticket(request): 

    form = TicketForm()
    form.fields['event'].queryset = Event.objects.filter(company=request.user)
    form.fields['category'].queryset = PaymentCategories.objects.filter(company=request.user)

    if request.method == 'POST':  
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ticket')

    context = {
        'form':form,
    }        


    return render(request, 'tickets/events.html', context)

@login_required
def host_dash(request):  

    events = Event.objects.filter(company=request.user)
    tickets = Ticket.objects.filter(event__in=events)
    categories = PaymentCategories.objects.filter(company=request.user)
    reservations = Reservation.objects.filter(ticket__in=tickets)

    context = {
        'events':events,
        'tickets':tickets,
        'reservations':reservations,
        'categories':categories,
    }

    return render(request, 'tickets/hostdash.html', context)

@login_required
def host_events(request):  

    events_list = Event.objects.filter(company=request.user).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(events_list, 8)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)


    context = {
        'events':events,
    }

    return render(request, 'tickets/adminEvents.html', context)    

@login_required
def host_event_edit(request, id):
    event = get_object_or_404( Event, id=id)

    form = EventForm(instance=event)
    form.fields['available_slots'].queryset = Slot.objects.filter(company=request.user)
    if request.method == 'POST':  
        form = EventForm(request.POST, request.FILES,instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.company = request.user
            event.save()
            return redirect('host_events')

    context = {
        'form':form,
        'event':event,
    }        


    return render(request, 'tickets/events.html', context)    

@login_required
def host_event_delete(request, id):
    event = get_object_or_404( Event, id=id)    
    event.delete()
    return redirect('host_events')


@login_required
def host_ticket_details(request, id):
    ticket = get_object_or_404( Ticket, id=id)

    reservations = Reservation.objects.filter(ticket=ticket).count()


    context = {
        'ticket':ticket,
        'reservations':reservations,
    }
    return render(request, 'tickets/adminT.html', context)

@login_required
def admin_ticket_edit(request, id): 
    ticket = get_object_or_404( Ticket, id=id)


    form = TicketForm(instance=ticket)
    form.fields['event'].queryset = Event.objects.filter(company=request.user)
    form.fields['category'].queryset = PaymentCategories.objects.filter(company=request.user)

    if request.method == 'POST':  
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('host_ticket_details' ,id=ticket.id)

    context = {
        'form':form,
        'ticket':ticket
    }        


    return render(request, 'tickets/adminTickets.html', context)

@login_required
def admin_ticket_delete(request, id): 
    ticket = get_object_or_404( Ticket, id=id)
    ticket.delete()
    return redirect('host_ticket_details', id=ticket.id)

def host_sales(request):

    rsvp_list = Reservation.objects.filter(ticket__event__company=request.user).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(rsvp_list, 10)

    try:
        reservations = paginator.page(page)
    except PageNotAnInteger:
        reservations = paginator.page(1)
    except EmptyPage:
        reservations = paginator.page(paginator.num_pages)

    context = {
        'reservations':reservations,
    }
    return render(request, 'tickets/hostsales.html', context)


@login_required
def site_admin(request):
    # all events RD
    # all reservations RD
    # register hosts

    if request.user.is_authenticated and request.user.is_staff:

        # reservations = Reservation.objects.all().order_by('-id')
        # events = Event.objects.all().order_by('-id')


        events_list = Event.objects.all().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(events_list, 10)

        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)

        rsvp_list = Reservation.objects.all().order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(rsvp_list, 10)

        try:
            reservations = paginator.page(page)
        except PageNotAnInteger:
            reservations = paginator.page(1)
        except EmptyPage:
            reservations = paginator.page(paginator.num_pages)

        context = {
            'reservations':reservations,
            'events':events,
        }

        return render(request, 'adm/index.html',context)  

    return redirect('index')      

@login_required
def site_admin_ticket_delete(request, id): 
    event = get_object_or_404( Event, id=id)    
    event.delete()
    return redirect('site_admin')

@login_required
def host_sales_delete(request, id): 
    rsvp = get_object_or_404( Reservation, id=id)    
    rsvp.delete()
    return redirect('host_sales')

@login_required
def site_admin_rsvp_delete(request, id): 
    rsvp = get_object_or_404( Reservation, id=id)    
    rsvp.delete()
    return redirect('site_admin')

@login_required
def site_admin_event_edit(request, id):
    event = get_object_or_404( Event, id=id)

    form = EventForm(instance=event)
    if request.method == 'POST':  
        form = EventForm(request.POST, request.FILES,instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.company = request.user
            event.save()
            return redirect('site_admin')

    context = {
        'form':form,
        'event':event,
    }        


    return render(request, 'tickets/events.html', context)   



from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from django.views.decorators.csrf import csrf_exempt
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword

def getAccessToken(request):
    consumer_key = 'AgWj2Q2HjMKx6rcfvUNA5GYfS8rfYMQ7'
    consumer_secret = 'STh3xNOGoLyAqiVe'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254742415221,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254742415221,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Events",
        "TransactionDesc": "Book ticket"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "http://127.0.0.1:8000/api/v1/c2b/confirmation",
               "ValidationURL": "http://127.0.0.1:8000/api/v1/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass

@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))
    

@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))    