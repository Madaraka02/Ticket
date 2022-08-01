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
        fields = ["name"]

class SlotForm(ModelForm):
        # menu = forms.ModelChoiceField(queryset=Menu.objects.filter(id=1))
    # category = forms.ModelChoiceField(queryset=PaymentCategories.objects.none(),)

    class Meta:
        model =  Slot   
        fields = ('theatre','category','number_of_seats','from_seat_number','to_seat_number',)

    # def __init__(self, *args, **kwargs):
    #     request = kwargs.pop('request', None)
    #     super().__init__(*args, **kwargs)
    #     if request:
    #         user = request.user
    #         self.fields['category'].queryset = PaymentCategories.objects.filter(company=user)

        # def __init__(self, user, *args, **kwargs):
        #     super(SlotForm, self).__init__(*args, **kwargs)
        #     self.fields['category'].queryset = PaymentCategories.objects.filter(company=user)

        # def __init__(self, *args, **kwargs):
        #     user = kwargs.pop('user','')
        #     super(SlotForm, self).__init__(*args, **kwargs)
        #     self.fields['category']=forms.ModelChoiceField(queryset=PaymentCategories.objects.filter(company=user))

class EventForm(ModelForm):
    # to include company -User
    # available_slots = forms.ModelMultipleChoiceField(queryset=Slot.objects.none(),)

    class Meta:
        model = Event
        fields = ['title','description','banner','date','starting_from','closed','available_slots']
        widgets = {
            'date': DateInput(attrs={'min': today}),
            'starting_from': TimePickerInput(),
            'description': forms.Textarea(attrs={'cols':4, 'rows':6}),

        } 

        # def __init__(self, user, *args, **kwargs):
        #     super(EventForm, self).__init__(*args, **kwargs)
        #     self.fields['available_slots'].queryset = PaymentCategories.objects.filter(company=user)

class TicketForm(ModelForm):
    # to include Event
    # event = forms.ModelChoiceField(queryset=Event.objects.none(),)
    # category = forms.ModelChoiceField(queryset=PaymentCategories.objects.none(),)


    class Meta:
        model = Ticket
        fields = ['event','category','price']     

                # def __init__(self, user, *args, **kwargs):
        #     super(EventForm, self).__init__(*args, **kwargs)
        #     self.fields['available_slots'].queryset = PaymentCategories.objects.filter(company=user)  

class ReservationForm(ModelForm):
    # to include Ticket
    class Meta:
        model = Reservation
        fields = ['names','email','phone_number','row_no','column_no']