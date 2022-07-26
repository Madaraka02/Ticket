from django.forms import ModelForm
from .models import *
from django import forms
from datetime import date


class DateInput(forms.DateInput):
    input_type = 'date'

class TimePickerInput(forms.TimeInput):
    input_type = 'time'    

today = date.today()
  

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = "__all__"

class PaymentCategoriesForm(ModelForm):
    class Meta:
        model = PaymentCategories
        fields = "__all__"

class SlotForm(ModelForm):
    class Meta:
        model =  Slot   
        fields = '__all__'

class EventForm(ModelForm):
    # to include company -User
    class Meta:
        model = Event
        fields = ['owner','title','description','banner','date','starting_from','closed','available_slots']
        widgets = {
            'date': DateInput(attrs={'min': today}),
            'starting_from': TimePickerInput(),
        } 

class TicketForm(ModelForm):
    # to include Event
    class Meta:
        model = Ticket
        fields = '__all__'       

class ReservationForm(ModelForm):
    # to include Ticket
    class Meta:
        model = Reservation
        fields = ['names','email','phone_number']