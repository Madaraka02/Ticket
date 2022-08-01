from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

# Create your views here.
def index(request):
    events = Event.objects.filter(closed=False).order_by('-id')
    
    context = {
        'events':events,
    }
    return render(request, 'tickets/index.html', context)

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

def home(request):
    form = PaymentCategoriesForm()
    if request.method == 'POST':  
        form = PaymentCategoriesForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.company = request.user
            category.save()
            return redirect('home')



    context = {
        'form':form,
    }        


    return render(request, 'tickets/home.html', context)
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
            return redirect('slot')

    context = {
        'form':form,
    }        


    return render(request, 'tickets/slot.html', context)
    
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


    return render(request, 'tickets/ticket.html', context)

@login_required
def host_dash(request):  
    # All events
    # All active events
    # Ticket sales per Category
    # Link to create events
    # Total money generation
    return render(request, 'tickets/hostdash.html', context)