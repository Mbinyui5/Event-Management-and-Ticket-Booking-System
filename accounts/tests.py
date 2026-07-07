from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Notification


class AccountAndNotificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='member', email='member@example.com', password='StrongPass123!')
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='AdminPass123!')

    def test_user_can_delete_account_after_password_confirmation(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('delete_account'), {'password': 'StrongPass123!'})

        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_admin_can_publish_notification(self):
        self.client.force_login(self.admin)

        response = self.client.post(reverse('send_notification'), {
            'title': 'Maintenance Notice',
            'message': 'The platform will be down for 15 minutes.',
            'target': 'all',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Notification.objects.filter(title='Maintenance Notice').exists())
