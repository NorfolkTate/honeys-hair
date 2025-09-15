from django.test import TestCase
from datetime import date, time
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Service, Booking

class BookingFlowTests(TestCase):
    def setUp(self):
        User = get_user_model()
        # users
        self.user = User.objects.create_user(username="amy", password="pass123", email="a@example.com")
        self.other = User.objects.create_user(username="bob", password="pass123", email="b@example.com")
        self.staff = User.objects.create_user(username="staff", password="pass123", email="s@example.com", is_staff=True)
        # data
        self.service = Service.objects.create(name="Cut", description="Basic cut", price=25)
        self.today = date.today()
        self.t10 = time(10, 0)
        self.booking = Booking.objects.create(
            name=self.user.username, service=self.service, date=self.today, time=self.t10
        )

    # My bookings
    def test_my_bookings_requires_login(self):
        r = self.client.get(reverse("my_bookings"))
        self.assertEqual(r.status_code, 302)
        self.assertIn("/accounts/login/", r["Location"])

    def test_my_bookings_shows_only_current_users_bookings(self):
        # another user's booking at 11:00 should not appear for amy
        Booking.objects.create(name=self.other.username, service=self.service, date=self.today, time=time(11, 0))
        self.client.login(username="amy", password="pass123")
        r = self.client.get(reverse("my_bookings"))
        self.assertContains(r, "Cut")      # has her service
        self.assertNotContains(r, "11:00") # not the other user's row

    # Create
    def test_book_appointment_creates_booking_for_logged_in_user(self):
        self.client.login(username="amy", password="pass123")
        payload = {"name": "ignored", "service": self.service.id, "date": self.today, "time": "12:00"}
        self.client.post(reverse("book_appointment"), data=payload, follow=True)
        self.assertTrue(
            Booking.objects.filter(name="amy", service=self.service, date=self.today, time=time(12, 0)).exists()
        )

    # Edit
    def test_edit_booking_owner_only(self):
        url = reverse("edit_booking", args=[self.booking.pk])
        # not owner
        self.client.login(username="bob", password="pass123")
        self.assertEqual(self.client.get(url).status_code, 404)
        # owner can edit
        self.client.logout()
        self.client.login(username="amy", password="pass123")
        r = self.client.post(url, {"name": "ignored", "service": self.service.id, "date": self.today, "time": "13:15"}, follow=True)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.time, time(13, 15))

    # Cancel
    def test_cancel_booking_deletes_record(self):
        url = reverse("cancel_booking", args=[self.booking.pk])
        self.client.login(username="amy", password="pass123")
        self.client.post(url, follow=True)  # POST = confirm cancel
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())

    # Staff
    def test_staff_page_requires_staff(self):
        self.client.login(username="amy", password="pass123")
        r = self.client.get(reverse("all_bookings"))
        # user_passes_test redirects non staff to login by default
        self.assertIn(r.status_code, (302, 403))
        self.client.logout()
        self.client.login(username="staff", password="pass123")
        self.assertEqual(self.client.get(reverse("all_bookings")).status_code, 200)

    def test_update_status_staff_only(self):
        url = reverse("update_booking_status", args=[self.booking.pk])
        self.client.login(username="staff", password="pass123")
        self.client.post(url, {"status": "CONFIRMED"}, follow=True)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "CONFIRMED")