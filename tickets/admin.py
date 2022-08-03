from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MpesaPayment)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Reservation)
admin.site.register(Slot)
admin.site.register(PaymentCategories)
admin.site.register(Eticket)


