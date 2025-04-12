from django import forms
from .models import Booking, Slot

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['slot']