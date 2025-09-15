from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('services/', views.services, name='services'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'), # code helpfully explained by stackoverflow and ref. in readme 
    path('booking/<int:pk>/edit/', views.edit_booking, name='edit_booking'),
    path('staff/bookings/', views.all_bookings, name='all_bookings'),
]
