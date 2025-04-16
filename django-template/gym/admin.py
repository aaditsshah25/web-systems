from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Slot, Booking, Trainer, ClassType, SpecialClassSlot, TrainerBooking

# Add custom CSS to admin
class CustomAdminSite(AdminSite):
    def each_context(self, request):
        context = super().each_context(request)
        context['extra_css'] = [
            'admin/css/custom_admin.css',
        ]
        return context

# Replace the default admin site
admin.site.__class__ = CustomAdminSite

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

class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization')
    search_fields = ('name', 'specialization')

class ClassTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes')
    search_fields = ('name',)

class SpecialClassSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'class_type', 'trainer', 'available', 'capacity')
    list_filter = ('date', 'class_type', 'trainer')
    search_fields = ('class_type__name', 'trainer__name')

class TrainerBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'class_slot', 'booked_at')
    list_filter = ('class_slot__date', 'class_slot__class_type', 'class_slot__trainer')
    search_fields = ('user__username', 'class_slot__trainer__name')

gym_admin_site.register(Slot, SlotAdmin)
gym_admin_site.register(Booking, BookingAdmin)
gym_admin_site.register(Trainer, TrainerAdmin)
gym_admin_site.register(ClassType, ClassTypeAdmin)
gym_admin_site.register(SpecialClassSlot, SpecialClassSlotAdmin)
gym_admin_site.register(TrainerBooking, TrainerBookingAdmin)

# Also register with the default admin site
admin.site.register(Slot, SlotAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(ClassType, ClassTypeAdmin)
admin.site.register(SpecialClassSlot, SpecialClassSlotAdmin)
admin.site.register(TrainerBooking, TrainerBookingAdmin)