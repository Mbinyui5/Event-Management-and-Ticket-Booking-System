from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Event, Category
from .forms import EventForm

# REST API imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers

# Helper decorator for checking admin/staff role
def admin_required(view_func):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='login',
        redirect_field_name=None
    )
    return actual_decorator(view_func)


def event_list_view(request):
    """
    Displays published events, supporting search (by title, description, venue),
    category filtering, and pagination.
    """
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    events_queryset = Event.objects.filter(status='published')

    if query:
        events_queryset = events_queryset.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(venue__icontains=query)
        )

    if category_slug:
        events_queryset = events_queryset.filter(category__slug=category_slug)

    # Paginate: 6 events per page
    paginator = Paginator(events_queryset, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': query,
    }
    return render(request, 'events/event_list.html', context)


def event_detail_view(request, pk):
    """
    Displays the detailed information about a single event.
    """
    event = get_object_or_404(Event, pk=pk)
    # Allow staff to view drafts, but hide from regular users
    if event.status != 'published' and not request.user.is_staff:
        messages.error(request, "This event is not active or published.")
        return redirect('event_list')

    return render(request, 'events/event_detail.html', {'event': event})


@login_required
@admin_required
def event_create_view(request):
    """
    Allows admins to create a new event.
    """
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, f"Event '{event.title}' created successfully!")
            return redirect('event_detail', pk=event.pk)
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'title': 'Create Event'})


@login_required
@admin_required
def event_update_view(request, pk):
    """
    Allows admins to update an existing event.
    """
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f"Event '{event.title}' updated successfully!")
            return redirect('event_detail', pk=event.pk)
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form, 'title': f'Edit {event.title}'})


@login_required
@admin_required
def event_delete_view(request, pk):
    """
    Allows admins to delete an event.
    """
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        title = event.title
        event.delete()
        messages.success(request, f"Event '{title}' deleted successfully!")
        return redirect('event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})


# ==================================================
# Django REST Framework API Endpoint
# ==================================================

class EventSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    remaining_tickets = serializers.IntegerField(read_only=True)
    is_sold_out = serializers.BooleanField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'category_name', 
            'date', 'time', 'venue', 'capacity', 'ticket_price', 
            'status', 'remaining_tickets', 'is_sold_out'
        ]

@api_view(['GET'])
def api_event_list(request):
    """
    API endpoint that returns list of all published events.
    """
    events = Event.objects.filter(status='published')
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
