from django.db import models
# from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from inclusive_django_range_fields import InclusiveIntegerRangeField

from django.contrib.auth import get_user_model

User=get_user_model()

# Create your models here.
class Venue(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name



class PaymentCategories(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name

class Slot(models.Model):
    theatre = models.CharField(max_length=300, blank=True, null=True)
    category = models.ForeignKey(PaymentCategories, on_delete=models.CASCADE, null=True) 
    number_of_seats =  models.PositiveIntegerField()
    from_seat_number = models.PositiveIntegerField(null=True, blank=True)
    to_seat_number = models.PositiveIntegerField(null=True, blank=True)



    def __str__(self):
        return self.theatre




class Event(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    banner = models.FileField(upload_to="events/banners", null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    starting_from = models.TimeField(null=True, blank=True)
    closed = models.BooleanField(default=False)
    available_slots = models.ManyToManyField(Slot, blank=True)

    def __str__(self):
        return self.title

TICKET_CHOICES = (
    ("VVIP", "VVIP"),
    ("VIP", "VIP"),
    ("REGULAR", "REGULAR"),
    ("KIDS", "KIDS"),
    ("ADVANCED", "ADVANCED"),
)
class Ticket(models.Model):
    # ticket_type = models.CharField(max_length = 20,choices = TICKET_CHOICES, default = 'REGULAR')    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)   
    category = models.ForeignKey(PaymentCategories, on_delete=models.CASCADE, null=True) 
    price = models.PositiveIntegerField()
    # paid = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.ticket_type} going for {self.price}"

class Reservation(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)   
    names = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone_number = PhoneNumberField()

    def __str__(self):
        return f"{self.email} bought {self.ticket.category} ticket for {self.ticket.event.title}"


    
