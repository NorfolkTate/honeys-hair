from django.shortcuts import render, redirect  # code helpfully inspired by stackoverflow and referenced in Readme
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Service


@login_required
def book_appointment(request): 
    if request.method == 'POST':
        form = BookingForm(request.POST)  # code helpfully provided by Stackoverflow and referenced in Readme
        if form.is_valid():
            try:
                form.save()
            except Exception as e:  #POTENTIAL FIX FFFFFFFFFFF
                print("FORM SAVE ERROR:", e)
                raise
            return render(request, 'booking/success.html')
    else:
        form = BookingForm()

    return render(request, 'booking/book.html', {'form': form})

def services(request):
    all_services = Service.objects.all()
    
    return render(request, 'booking/services.html', {'services': all_services})