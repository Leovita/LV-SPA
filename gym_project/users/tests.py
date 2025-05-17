from django.test import TestCase
import json
from django.urls import reverse
from django.utils import timezone
from users.models import User
from palestra.models import GymClass, GymBooking

#test per la prenotazione di un corso palestra

class BookGymClassTest(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            email='istruttore@example.com',
            password='password123',
            full_name='Istruttore Test',
            is_staff=True
        )
        self.user = User.objects.create_user(
            email='utente@example.com',
            password='pass123',
            full_name='Utente Test'
        )
        self.gym_class = GymClass.objects.create(
            name='Yoga',
            description='Corso di Yoga',
            scheduled=timezone.now() + timezone.timedelta(days=1),
            duration=60,
            instructor=self.instructor,
            max_partecipants=10
        )

    def test_user_can_book_gym_class(self):
        self.client.login(email='utente@example.com', password='pass123')
        logged_in = self.client.login(email='utente@example.com', password='pass123')
        self.assertTrue(logged_in)
        url = reverse('book_gym', args=[self.gym_class.id])
        booking_time = (timezone.now() + timezone.timedelta(days=1)).isoformat()
        response = self.client.post(
            url,
            data=json.dumps({'date_time': booking_time}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertIn('booking_id', data)
        booking = GymBooking.objects.filter(user=self.user, class_id=self.gym_class).first()
        self.assertIsNotNone(booking)
