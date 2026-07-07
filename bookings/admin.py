from django.contrib import admin
from .models import Booking, Ticket

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'user', 'event', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('booking_reference', 'user__username', 'event__title')
    ordering = ('-created_at',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'event', 'booking', 'is_checked_in', 'created_at')
    list_filter = ('is_checked_in', 'created_at')
    search_fields = ('ticket_number', 'ticket_reference', 'booking__booking_reference', 'event__title')
    ordering = ('-created_at',)
