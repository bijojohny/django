from datetime import timezone

from django.db import models
from django.contrib.auth.models import User

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)


class TourPackage(models.Model):  # Inherits from models.Model
    title = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    duration = models.IntegerField()
    image = models.ImageField(upload_to='static/images/', null=True, blank=True)  # New ImageField
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tour_packages')
    approved = models.BooleanField(default=False)  # Admin approval field

    def _str_(self):
        return self.title

class Package(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()  # duration in days
    destination = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_approved = models.BooleanField(default=False)

    def has_expired(self):
        return self.expiry_date < timezone.now().date()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    number_of_people = models.IntegerField()
    status = models.CharField(max_length=50, default="Pending")


class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)