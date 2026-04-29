from django.db import models

# Create your models here.
from accounts.models import User
from services.models import Service

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_bookings')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.TimeField()

    address = models.CharField(max_length=100, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} → {self.freelancer} ({self.status})"
class Review(models.Model):
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE)
    client = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='reviews_given')
    freelancer = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='reviews_received')

    rating = models.IntegerField()  # 1 to 5 stars
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}★ - {self.freelancer.username}"