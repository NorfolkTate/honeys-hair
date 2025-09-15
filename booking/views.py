from django.shortcuts import render, redirect, get_object_or_404  # code helpfully inspired by stackoverflow and referenced in Readme
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import BookingForm
from .models import Service, Booking
from django.core.mail import send_mail
from django.contrib.auth import get_user_model



@login_required

@user_passes_test(lambda u: u.is_staff)
def all_bookings(request):
 # COME BACK TO THIS BIT
    bookings = Booking.objects.select_related("service").order_by("date", "time")
    return render(request, "booking/all_bookings.html", {"bookings": bookings})

def update_booking_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        valid = [s[0] for s in Booking.STATUS_CHOICES]
        if new_status in valid:
            if booking.status != new_status:
                booking.status = new_status
                booking.save(update_fields=["status"])
                messages.success(request, "Booking updated")

                try:
                    User = get_user_model()
                    user = User.objects.get(username=booking.name)
                    if user.email:
                        send_mail(
                            subject="Your Honey's Hair booking status was updated",
                            message=(
                                f"Hi {user.username},\n\n"
                                f"Your booking for {booking.service.name} on {booking.date} at {booking.time} "
                                f"is now '{booking.get_status_display()}'.\n\n"
                                "Thanks,\nHoney's Hair"
                            ),
                            from_email=None,
                            recipient_list=[user.email],
                            fail_silently=True,
                        )
                except User.DoesNotExist:
                    pass
            else:
                messages.info(request, "Status is unchanged")
        else:
            messages.error(request, "Invalid")
    return redirect("all_bookings")

def my_bookings(request):
    bookings = Booking.objects.filter(name=request.user.username).order_by("date", "time")
    return render(request, "booking/my_bookings.html", {
        "bookings": bookings,
    })

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


