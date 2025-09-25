from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100) # code helpfully inspired by python programming tutorials and referenced in Readme
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Booking(models.Model):

    STATUS_PENDING   = "PENDING"
    STATUS_CONFIRMED = "CONFIRMED"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE) #code helpfully inspired by StackOverflow and referenced in Readme
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    def __str__(self):
        return f"{self.name} - {self.service} on {self.date} at {self.time}"