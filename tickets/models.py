from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
VENUE_CHOICES = (
    ("VVIP", "VVIP"),
    ("VIP", "VIP"),
    ("REGULAR", "REGULAR"),
    ("KIDS", "KIDS"),
    ("ADVANCED", "ADVANCED"),
)
class Venue(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    category = models.CharField(max_length = 20,choices = VENUE_CHOICES, default = 'REGULAR')   
    number_of_seats =  models.PositiveIntegerField()

    def __str__(self):
        return f"{self.category} has {self.number_of_seats} seats"




class Event(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.CharField(max_length=300, blank=True, null=True)
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    banner = models.FileField(upload_to="events/banners", null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    closed = models.BooleanField(default=False)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

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
    ticket_type = models.CharField(max_length = 20,choices = TICKET_CHOICES, default = 'REGULAR')    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)   
    price = models.PositiveIntegerField()
    paid = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.ticket_type} going for {self.price}"

class Reservation(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)   
    names = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone_number = PhoneNumberField()

    def __str__(self):
        return f"{self.email} bought {ticket.ticket_type} ticket for {ticket.event.title}"


    
