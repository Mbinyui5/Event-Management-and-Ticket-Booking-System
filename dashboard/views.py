import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q
from django.http import HttpResponse
from events.models import Event, Category
from bookings.models import Booking
from accounts.forms import NotificationForm
from accounts.models import Notification
from events.views import admin_required

@login_required
@admin_required
def admin_dashboard_view(request):
    """
    Computes aggregates for the executive dashboard:
    - total registered users, bookings, revenue, active events
    - category & event distribution for Chart.js
    - recent activity feed & users list for new UI panels
    """
    total_users    = User.objects.count()
    total_bookings = Booking.objects.filter(status='confirmed').count()
    total_categories = Category.objects.count()

    # Sold-out events
    all_events = Event.objects.filter(status='published')
    sold_out_events = sum(1 for e in all_events if e.is_sold_out)

    # Revenue
    revenue_agg  = Booking.objects.filter(status='confirmed').aggregate(
        total_rev=Sum('event__ticket_price')
    )
    total_revenue = revenue_agg['total_rev'] or 0.00

    active_events = Event.objects.filter(status='published').count()

    # Management table data
    events_list   = Event.objects.all().order_by('-created_at').select_related('category')
    bookings_list = Booking.objects.all().order_by('-created_at').select_related('user', 'event', 'event__category')

    # Recent activity feed (last 8)
    recent_bookings = Booking.objects.all().order_by('-created_at')[:8].select_related('user', 'event')

    # Users list for the users tab
    users_list = User.objects.all().order_by('-date_joined')

    # Chart.js: Booking distribution by Category
    categories_data = Category.objects.annotate(
        booking_count=Count(
            'events__bookings',
            filter=Q(events__bookings__status='confirmed')
        )
    ).values('name', 'booking_count')

    category_labels = [cat['name'] for cat in categories_data]
    category_counts = [cat['booking_count'] for cat in categories_data]

    # Chart.js: Revenue per Event (Top 6)
    top_events = Event.objects.annotate(
        event_revenue=Sum(
            'bookings__event__ticket_price',
            filter=Q(bookings__status='confirmed')
        )
    ).filter(event_revenue__gt=0).order_by('-event_revenue')[:6]

    event_labels   = [evt.title[:25] + ('…' if len(evt.title) > 25 else '') for evt in top_events]
    event_revenues = [float(evt.event_revenue or 0) for evt in top_events]

    notification_form = NotificationForm()

    context = {
        'total_users':       total_users,
        'total_bookings':    total_bookings,
        'total_revenue':     total_revenue,
        'active_events':     active_events,
        'total_categories':  total_categories,
        'sold_out_events':   sold_out_events,
        'events_list':       events_list,
        'bookings_list':     bookings_list,
        'recent_bookings':   recent_bookings,
        'users_list':        users_list,
        'category_labels':   category_labels,
        'category_counts':   category_counts,
        'event_labels':      event_labels,
        'event_revenues':    event_revenues,
        'notification_form': notification_form,
        'notifications':     Notification.objects.filter(is_active=True).order_by('-created_at')[:6],
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
@admin_required
def send_notification_view(request):
    """
    Allows admins to publish a notification to all users.
    """
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.created_by = request.user
            notification.save()
            messages.success(request, 'Notification published successfully.')
        else:
            messages.error(request, 'Please correct the notification form and try again.')
        return redirect('admin_dashboard')

    return redirect('admin_dashboard')


@login_required
@admin_required
def export_report_view(request):
    """
    Generates dynamic CSV reports based on filters:
    - Event (id), Category (slug), Status
    """
    event_id      = request.GET.get('event')
    category_slug = request.GET.get('category')
    status        = request.GET.get('status')

    bookings = Booking.objects.all().select_related('user', 'event', 'event__category')

    if event_id:
        bookings = bookings.filter(event_id=event_id)
    if category_slug:
        bookings = bookings.filter(event__category__slug=category_slug)
    if status:
        bookings = bookings.filter(status=status)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ticket_sales_report.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Booking Reference', 'Customer Username', 'Customer Email',
        'Event Title', 'Event Category', 'Ticket Price (FCFA)',
        'Booking Status', 'Payment Status', 'Booking Date'
    ])

    for booking in bookings:
        writer.writerow([
            booking.booking_reference,
            booking.user.username,
            booking.user.email,
            booking.event.title,
            booking.event.category.name,
            booking.event.ticket_price,
            booking.status,
            booking.payment_status,
            booking.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response
