from django import forms
from .models import Booking

class BookingForm(forms.ModelForm): # code helpfully inspired by Reddit and referenced in Readme 
    class Meta: # code explained provided by code institute tutorials
        model = Booking
        fields = ['name', 'service', 'date', 'time']
        widgets = { # code explained and provided by django documentation and refernced in Readme
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }