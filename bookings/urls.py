from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:event_id>/', views.book_ticket_view, name='book_ticket'),
    path('confirmation/<uuid:booking_ref>/', views.booking_confirmation_view, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings_view, name='my_bookings'),
]
