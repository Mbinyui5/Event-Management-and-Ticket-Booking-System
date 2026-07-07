import uuid
from django.db import models
from django.contrib.auth.models import User
from events.models import Event

class Booking(models.Model):
    """
    Represents a ticket purchase transaction by a user.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]

    booking_reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='paid')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking {self.booking_reference} - {self.user.username}"


class Ticket(models.Model):
    """
    Represents the actual entrance ticket linked to a verified booking.
    """
    ticket_reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='ticket')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_number = models.CharField(max_length=50, unique=True, blank=True)
    is_checked_in = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate custom human-readable ticket number if not set
        if not self.ticket_number:
            uid = str(uuid.uuid4()).split('-')[0].upper()
            self.ticket_number = f"TKT-{self.event.id}-{uid}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_number
