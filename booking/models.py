from django.db import models

# Create your models here.

class Booking(models.Model):
    name = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.service} on {self.date} at {self.time}"
