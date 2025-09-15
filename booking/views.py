from django.shortcuts import render, redirect, get_object_or_404  # code helpfully inspired by stackoverflow and referenced in Readme
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

def edit_booking(request, pk):
# COME BACK TO THIS BIT
    booking = get_object_or_404(Booking, pk=pk, name=request.user.username)

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.name = request.user.username  # user
            obj.save()
            messages.success(request, "Booking updated")
            return redirect("my_bookings")
    else:
        form = BookingForm(instance=booking)
        #same form
    return render(request, "booking/book.html", {"form": form, "editing": True})

def cancel_booking(request, pk):
# COME BACK TO THIS BIT
    booking = get_object_or_404(Booking, pk=pk, name=request.user.username) #Code provided by stackoverflow and ref. in readme
    # code provided by geeks for geeks and ref. in readme 

    if request.method == "POST":
        booking.delete()
        messages.info(request, "Your booking has been cancelled")
        return redirect("my_bookings")

    return render(request, "booking/confirm_cancel.html", {"booking": booking})

def services(request):
    all_services = Service.objects.all()

    return render(request, 'booking/services.html', {'services': all_services})

def home(request):
    
    return render(request, 'booking/home.html')
