from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Slot, Booking

class GymAdminSite(AdminSite):
    site_header = 'Gym Booking Administration'
    site_title = 'Gym Booking Admin'
    index_title = 'Gym Management'

gym_admin_site = GymAdminSite(name='gym_admin')

# Register your models with the custom admin site
class SlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'capacity', 'available')
    list_filter = ('date',)
    search_fields = ('date',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'slot', 'booked_at')
    list_filter = ('slot__date', 'booked_at')
    search_fields = ('user__username',)

gym_admin_site.register(Slot, SlotAdmin)
gym_admin_site.register(Booking, BookingAdmin)

# Also register with the default admin site
admin.site.register(Slot, SlotAdmin)
admin.site.register(Booking, BookingAdmin)