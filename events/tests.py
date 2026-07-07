from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from events.models import Event


class SeedDataCommandTests(TestCase):
    def test_seed_data_adds_featured_events_and_more_catalogue_items(self):
        call_command('seed_data', stdout=StringIO())

        featured_titles = [
            'COLTECH HACKATHON',
            'NAHPI HACKATHON',
            'Frontend Dev Masterclass',
            'Backend Dev Bootcamp',
        ]

        for title in featured_titles:
            self.assertTrue(
                Event.objects.filter(title__icontains=title).exists(),
                f'Missing featured event: {title}',
            )

        self.assertGreaterEqual(
            Event.objects.filter(status='published').count(),
            15,
            'Expected the seed data to provide a richer event catalog.',
        )
