from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Reservation)
admin.site.register(Slot)

