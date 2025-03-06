from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from push_notifications.models import GCMDevice
import uuid

User = get_user_model()

class Bus(models.Model):
    status_choices = (
        ("AVAILABLE", "AVAILABLE"),
        ("UNAVAILABLE", "UNAVAILABLE")
    )
    bus_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    bus_name = models.CharField(max_length=30)
    number = models.CharField(max_length=15, unique=True)
    start = models.CharField(max_length=30)
    stop = models.CharField(max_length=30)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    total_seats = models.PositiveIntegerField()
    status = models.CharField(max_length=15, choices=status_choices, default="AVAILABLE")
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bus_name} From {self.start} To {self.stop}: {self.departure}"


class Book(models.Model):
    STATUS_CHOICES = (
        ("ACTIVE", "ACTIVE"),
        ("WAITING", "WAITING"),
        ("CLOSED", "CLOSED")
    )

    book_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="owner", verbose_name="Ticket Owner")
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="book")
    seat = models.IntegerField(default=0)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    status = models.CharField(max_length=225, choices=STATUS_CHOICES, blank=True, null=True, default="WAITING")
    assigned_to = models.ForeignKey(User, blank=True, null=True, verbose_name="Assigned to", on_delete=models.CASCADE)
    closed_date = models.DateTimeField(blank=True, null=True)
    archived = models.BooleanField(default=False)
    attached = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class META:
        unique_together = ("bus", "seat")

    def __str__(self):
        return f"NAME: {self.full_name}, \nBUS: {self.bus.bus_name}, SEAT: {self.seat}, FROM: {self.bus.start}, TO: {self.bus.stop}, CREATED_AT: {self.created_at}"


class Attachment(models.Model):
    attach_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images", max_length=1000)
    attached = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Attachment for Ticket: {self.book.full_name} by {self.book.user.username}"


class Device(GCMDevice):
    notification_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_user", verbose_name="Notifications")


class Service(models.Model):
    service_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=500)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} : {self.description}"