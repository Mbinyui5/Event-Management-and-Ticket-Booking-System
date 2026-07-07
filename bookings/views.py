import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from events.models import Event
from .models import Booking, Ticket

@login_required
def book_ticket_view(request, event_id):
    """
    Handles booking a ticket for an event.
    Uses database row-locking (select_for_update) within an atomic transaction
    to absolutely prevent overbooking due to concurrent requests.
    """
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Lock the event row for updates during this transaction
                event = Event.objects.select_for_update().get(pk=event_id)

                # Validation checks
                if event.status != 'published':
                    messages.error(request, "This event is currently not open for bookings.")
                    return redirect('event_detail', pk=event.pk)

                # Check current confirmed bookings count
                confirmed_bookings_count = Booking.objects.filter(event=event, status='confirmed').count()
                
                if confirmed_bookings_count >= event.capacity:
                    messages.error(request, "Sorry, this event is already sold out!")
                    return redirect('event_detail', pk=event.pk)

                # Create the Booking record
                booking = Booking.objects.create(
                    user=request.user,
                    event=event,
                    status='confirmed',
                    payment_status='paid'
                )

                # Create the Ticket record
                ticket = Ticket.objects.create(
                    booking=booking,
                    event=event
                )

                messages.success(request, f"Successfully booked ticket for {event.title}!")
                return redirect('booking_confirmation', booking_ref=booking.booking_reference)

        except Event.DoesNotExist:
            messages.error(request, "The event does not exist.")
            return redirect('event_list')
        except Exception as e:
            messages.error(request, f"An error occurred during booking: {str(e)}")
            return redirect('event_detail', pk=event_id)

    # GET requests are redirected to event detail page
    return redirect('event_detail', pk=event_id)


@login_required
def booking_confirmation_view(request, booking_ref):
    """
    Renders the booking confirmation page containing the digital ticket,
    complete with booking details and a dynamically generated QR Code (base64 encoded).
    """
    booking = get_object_or_404(Booking, booking_reference=booking_ref)
    
    # Restrict viewing to the owner or staff members
    if booking.user != request.user and not request.user.is_staff:
        messages.error(request, "You do not have permission to view this ticket.")
        return redirect('event_list')

    # Generate QR Code representing the ticket validation data
    qr_data = f"REF:{booking.booking_reference}|TKT:{booking.ticket.ticket_number if hasattr(booking, 'ticket') else 'N/A'}|EVT:{booking.event.title}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#1e293b", back_color="white")  # Slate-800 to match theme
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    context = {
        'booking': booking,
        'qr_code_base64': qr_base64
    }
    return render(request, 'bookings/booking_confirmation.html', context)


@login_required
def my_bookings_view(request):
    """
    Displays list of bookings belonging to the logged-in user.
    """
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})
