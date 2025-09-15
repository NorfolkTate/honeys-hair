from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('services/', views.services, name='services'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
