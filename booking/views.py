from django.shortcuts import render, redirect # code helpfully inspired by stackoverflow and referenced in Readme 

# Create your views here.

from .forms import BookingForm

def book_appointment(request): 
    if request.method == 'POST':
        form = BookingForm(request.POST) # code helpfully provided by Stackoverflow and referenced in Readme
        if form.is_valid():
            form.save()
            return redirect()
    else:
        form = BookingForm()
    
    return render(request)
