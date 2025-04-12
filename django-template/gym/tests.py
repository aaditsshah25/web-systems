from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Slot, Booking

class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        self.slot = Slot.objects.create(
            date=timezone.now().date(),
            start_time='10:00',
            end_time='11:00'
        )

    def test_slot_creation(self):
        self.assertTrue(isinstance(self.slot, Slot))
        self.assertEqual(self.slot.available, 10)

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_not_found_url(self):
        response = self.client.get('/a-url-that-does-not-exist')
        self.assertEquals(response.status_code, 404)