from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import json 
from users.models import User
from palestra.models import GymClass, GymBooking
from spa.models import SpaService, SpaBooking

class UserBookingTests(TestCase):
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
        self.spa_service = SpaService.objects.create(
            name='Massaggio',
            description='Massaggio rilassante',
            operator=self.instructor,
            duration=60,
            price=50,
            max_partecipants=1,
            scheduled=timezone.now() + timezone.timedelta(days=1),
            type='massage'
        )

    def test_user_can_book_gym_class(self):
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

    def test_user_can_cancel_gym_booking(self):
        logged_in = self.client.login(email='utente@example.com', password='pass123')
        self.assertTrue(logged_in)
        booking = GymBooking.objects.create(
            user=self.user,
            class_id=self.gym_class,
            date=timezone.now() + timezone.timedelta(days=1)
        )
        url = reverse('cancel_gym_booking', args=[booking.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))
        exists = GymBooking.objects.filter(id=booking.id).exists()
        self.assertFalse(exists)

    def check_credential_error(self):
        logged_in = self.client.login(email='utente@example.com', password='pass123')
        self.assertTrue(logged_in)
        url = reverse('book_gym', args=[self.gym_class.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 401)
        return response

    def test_login_view(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # redirect to /login/?tab=register

    def test_logout_view(self):
        self.client.login(email='utente@example.com', password='pass123')
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_profile_view_requires_login(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # redirect to login
        self.client.login(email='utente@example.com', password='pass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_gest_corsi_staff(self):
        self.client.login(email='istruttore@example.com', password='password123')
        url = reverse('gest_corsi')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_gest_prenotazioni_staff(self):
        self.client.login(email='istruttore@example.com', password='password123')
        url = reverse('gest_prenotazioni')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_ajax_ok_and_error(self):
        from users.views.utils import ajax_ok, ajax_error
        resp_ok = ajax_ok('ok')
        resp_err = ajax_error('errore')
        self.assertEqual(resp_ok.status_code, 200)
        self.assertEqual(resp_err.status_code, 200)
        self.assertIn('success', resp_ok.content.decode())
        self.assertIn('error', resp_err.content.decode())

