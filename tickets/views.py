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
            return redirect('host_dash')



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
            return redirect('host_dash')

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

    events = Event.objects.filter(company=request.user).order_by('-id')

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