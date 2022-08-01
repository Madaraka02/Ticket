from django.db import models
# from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from inclusive_django_range_fields import InclusiveIntegerRangeField
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model

User=get_user_model()

# Create your models here.
class Venue(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name



class PaymentCategories(models.Model):
    company = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name

class Slot(models.Model):
    theatre = models.CharField(max_length=300, blank=True, null=True)
    category = models.ForeignKey(PaymentCategories, on_delete=models.CASCADE, null=True) 
    number_of_seats =  models.PositiveIntegerField()
    from_seat_number = models.PositiveIntegerField(null=True, blank=True)
    to_seat_number = models.PositiveIntegerField(null=True, blank=True)
    company = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    
    @property
    def seats(self):
        available_seats = [seat for seat in range((self.from_seat_number), (self.to_seat_number +1))]
        return available_seats

    @property
    def numberOfSeats(self):
        # available_seats = [seat for seat in range((self.from_seat_number), (self.to_seat_number +1))]
        return len(self.seats)

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


    def __str__(self):
        return f"{self.category.name} going for {self.price}"

class Reservation(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)   
    names = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    phone_number = PhoneNumberField()
    row_no = models.CharField(max_length=5, null=True, blank=True) 
    column_no = models.CharField(max_length=5, null=True, blank=True) 

    paid = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.email} reserved {self.ticket.category}"


    
class Eticket(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE) 
    seat_no = models.CharField(max_length=20, null=True, blank=True)     
    ticket_class = models.CharField(max_length=20, null=True, blank=True)  

    def __str__(self):
        return f"{self.reservation.names} {self.seat_no} {self.ticket_class}"

# lisst = [1,2,3,4,5]
# for i in range(len(lisst)-1):
#     del lisst[0]

# [2, 3, 4, 5]
# [3, 4, 5]
# [4, 5]
# [5]

@receiver(post_save, sender=Reservation)
def create_eticket(sender, instance, created, **kwargs):
    if created:
        slots = [slot for slot in instance.ticket.event.available_slots.all() if slot.category == instance.ticket.category]
        aseats=[i.seats for i in slots][0]
        seat_no=aseats[0]
        Eticket.objects.create(reservation=instance,ticket_class=str(instance.ticket.category),
        seat_no=seat_no)
        # del aseats[0]

@receiver(post_save, sender=Reservation)
def save_eticket(sender, instance, **kwargs):
    instance.eticket.save()

