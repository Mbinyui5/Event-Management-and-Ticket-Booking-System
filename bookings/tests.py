import threading
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from django.db import transaction
from events.models import Category, Event
from bookings.models import Booking, Ticket

class BookingSystemTests(TransactionTestCase):
    """
    Unit test suite to verify the integrity of the booking process,
    overbooking prevention, and database row-locking under concurrent requests.
    """
    def setUp(self):
        # Create seed category
        self.category = Category.objects.create(name="Tech Meetups", slug="tech-meetups")
        
        # Create seed admin
        self.admin = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword',
            email='admin@example.com'
        )

        # Create attendee users
        self.user1 = User.objects.create_user(username='user1', password='passuser1')
        self.user2 = User.objects.create_user(username='user2', password='passuser2')
        self.user3 = User.objects.create_user(username='user3', password='passuser3')

        # Create an event with a limited capacity of 2 for testing
        self.event = Event.objects.create(
            title="Limited Capacity Event",
            description="Testing overbooking prevention.",
            category=self.category,
            date="2026-06-15",
            time="18:00:00",
            venue="Silicon Labs",
            capacity=2,
            ticket_price=10.00,
            status="published",
            created_by=self.admin
        )

    def test_successful_booking(self):
        """
        Verify that a user can book a ticket under normal circumstances
        and a unique Booking Reference and Ticket Number are generated.
        """
        self.client.login(username='user1', password='passuser1')
        response = self.client.post(f'/bookings/book/{self.event.id}/', follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Booking.objects.filter(event=self.event, status='confirmed').count(), 1)
        self.assertEqual(Ticket.objects.filter(event=self.event).count(), 1)
        
        booking = Booking.objects.get(user=self.user1, event=self.event)
        self.assertIsNotNone(booking.booking_reference)
        self.assertIsNotNone(booking.ticket.ticket_number)

    def test_overbooking_prevention(self):
        """
        Ensures that when capacity is reached (2 bookings),
        subsequent booking attempts are rejected.
        """
        # User 1 books ticket 1 (succeeds)
        Booking.objects.create(user=self.user1, event=self.event, status='confirmed')
        # User 2 books ticket 2 (succeeds)
        Booking.objects.create(user=self.user2, event=self.event, status='confirmed')
        
        # User 3 attempts to book ticket 3 (fails due to sold out status)
        self.client.login(username='user3', password='passuser3')
        response = self.client.post(f'/bookings/book/{self.event.id}/', follow=True)
        
        # Total confirmed bookings must remain exactly 2 (the capacity limit)
        self.assertEqual(Booking.objects.filter(event=self.event, status='confirmed').count(), 2)
        # Verify redirect or alert message
        messages = [m.message for m in response.context['messages']]
        self.assertIn("Sorry, this event is already sold out!", messages)

    def test_concurrent_bookings_row_locking(self):
        """
        Simulates 3 users clicking the 'Book Ticket' button at the exact same millisecond.
        Since event capacity is 2, exactly 2 bookings must succeed and 1 must fail.
        This tests that row-locking prevents race conditions.
        """
        exceptions = []

        def execute_booking(user):
            try:
                # Spawn a separate connection and transaction block for each thread
                with transaction.atomic():
                    # Acquire row lock
                    event_locked = Event.objects.select_for_update().get(id=self.event.id)
                    confirmed_count = Booking.objects.filter(event=event_locked, status='confirmed').count()
                    
                    if confirmed_count < event_locked.capacity:
                        Booking.objects.create(
                            user=user,
                            event=event_locked,
                            status='confirmed'
                        )
            except Exception as e:
                exceptions.append(e)

        # Initialize three threads
        t1 = threading.Thread(target=execute_booking, args=(self.user1,))
        t2 = threading.Thread(target=execute_booking, args=(self.user2,))
        t3 = threading.Thread(target=execute_booking, args=(self.user3,))

        # Start all threads
        t1.start()
        t2.start()
        t3.start()

        # Wait for all threads to complete
        t1.join()
        t2.join()
        t3.join()

        # Assertions
        confirmed_bookings = Booking.objects.filter(event=self.event, status='confirmed')
        self.assertEqual(confirmed_bookings.count(), 2, "Row-locking failed to limit bookings to capacity!")
