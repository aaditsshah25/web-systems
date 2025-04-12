from django.contrib import admin
from .models import Slot, Booking

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'start_time', 'end_time', 'capacity', 'available')
    list_filter = ('date',)
    search_fields = ('date',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slot', 'booked_at')
    list_filter = ('booked_at', 'slot__date')
    search_fields = ('user__username',)