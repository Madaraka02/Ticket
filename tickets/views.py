from django.shortcuts import render, redirect, get_object_or_404
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


def home(request):
    form = PaymentCategoriesForm()
    if request.method == 'POST':  
        form = PaymentCategoriesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')



    context = {
        'form':form,
    }        


    return render(request, 'tickets/home.html', context)

def slot(request): 

    form = SlotForm()
    if request.method == 'POST':  
        form = SlotForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('slot')

    context = {
        'form':form,
    }        


    return render(request, 'tickets/slot.html', context)
    
def event(request): 

    form = EventForm()
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
    if request.method == 'POST':  
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ticket')

    context = {
        'form':form,
    }        


    return render(request, 'tickets/ticket.html', context)