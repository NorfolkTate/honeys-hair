from django.shortcuts import render, redirect  # code helpfully inspired by stackoverflow and referenced in Readme
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from .models import Service, Booking


@login_required

def my_bookings(request):
    # logged in user
    qs = Booking.objects.filter(name=request.user.username).order_by("date", "time")
    return render(request, "booking/my_bookings.html", {"bookings": qs})

def book_appointment(request): 
    if request.method == 'POST':
        form = BookingForm(request.POST)  # code helpfully provided by Stackoverflow and referenced in Readme
        if form.is_valid():
            booking = form.save(commit=False)   # don’t save yet
            booking.name = request.user.username  # link booking to logged in user
            booking.save()
            return render(request, 'booking/success.html')
    else:
        form = BookingForm()

    return render(request, 'booking/book.html', {'form': form})

def services(request):
    all_services = Service.objects.all()

    return render(request, 'booking/services.html', {'services': all_services})

def home(request):
    
    return render(request, 'booking/home.html')
