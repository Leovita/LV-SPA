from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

#test funzionalità di codice applicativo
class RegistrationTests(TestCase):
    def setUp(self):
        """Setup iniziale per ogni test"""
        self.client = Client()
        self.register_url = reverse('register')
        
    def test_empty_fields(self):
        """Test 1: Verifica che la registrazione fallisca con campi vuoti"""
        #richiesta POST con fields vuoti
        response = self.client.post(self.register_url, {})
        
        #la risposta sia un redirect 
        self.assertEqual(response.status_code, 302)
        #non sia stato creato alcun utente
        self.assertEqual(User.objects.count(), 0)
        #il messaggio di errore sia corretto
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any('compila tutti i campi' in str(msg).lower() for msg in messages_list))

    def test_invalid_email(self):
        """Test 2: Verifica che la registrazione fallisca con email non valida"""
        #richiesta POST con email non valida
        response = self.client.post(self.register_url, {
            'register-name': 'Test User',
            'register-email': 'invalid-email',
            'register-password': 'Test123!',
            'register-confirm': 'Test123!'
        })
        
        #la risposta sia un redirect
        self.assertEqual(response.status_code, 302)
        #non sia stato creato alcun utente
        self.assertFalse(User.objects.filter(email='invalid-email').exists())
        #il messaggio di errore sia corretto
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any('email non valida' in str(msg).lower() for msg in messages_list))

    def test_existing_email(self):
        """Test 3: Verifica che la registrazione fallisca con email già esistente"""
        #crea un utente esistente
        User.objects.create_user(
            email='existing@test.com',
            password='Test123!',
            full_name='Existing User'
        )
        
        #richiesta POST con email già esistente
        response = self.client.post(self.register_url, {
            'register-name': 'Test User',
            'register-email': 'existing@test.com',
            'register-password': 'Test123!',
            'register-confirm': 'Test123!'
        })
        
        #la risposta sia un redirect
        self.assertEqual(response.status_code, 302)
        #non sia stato creato un nuovo utente con la stessa email
        self.assertEqual(User.objects.filter(email='existing@test.com').count(), 1)
        #il messaggio di errore sia corretto
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any('utente già esistente' in str(msg).lower() for msg in messages_list))

    def test_password_no_uppercase(self):
        """Test 5: Verifica che la registrazione fallisca con password senza maiuscola"""
        response = self.client.post(self.register_url, {
            'register-name': 'Test User',
            'register-email': 'nomaiuscola@test.com',
            'register-password': 'test1234!',
            'register-confirm': 'test1234!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='nomaiuscola@test.com').exists())
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any('maiuscola' in str(msg).lower() for msg in messages_list))

    def test_password_no_number(self):
        """Test 6: Verifica che la registrazione fallisca con password senza numero"""
        response = self.client.post(self.register_url, {
            'register-name': 'Test User',
            'register-email': 'nonumero@test.com',
            'register-password': 'TestTest!',
            'register-confirm': 'TestTest!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='nonumero@test.com').exists())
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any('numero' in str(msg).lower() for msg in messages_list))

    def test_password_no_special(self):
        """Test 7: Verifica che la registrazione fallisca con password senza simbolo speciale"""
        response = self.client.post(self.register_url, {
            'register-name': 'Test User',
            'register-email': 'nospeciale@test.com',
            'register-password': 'Test1234',
            'register-confirm': 'Test1234'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='nospeciale@test.com').exists())
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any('simbolo speciale' in str(msg).lower() for msg in messages_list))

    def test_password_mismatch(self):
        """Test 8: Verifica che la registrazione fallisca con password e conferma non coincidenti"""
        response = self.client.post(self.register_url, {
            'register-name': 'Test User',
            'register-email': 'mismatch@test.com',
            'register-password': 'Test123!',
            'register-confirm': 'Test1234!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='mismatch@test.com').exists())
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any('password non coincidono' in str(msg).lower() for msg in messages_list))

    def test_short_name(self):
        """Test 9: Verifica che la registrazione fallisca con nome troppo corto"""
        response = self.client.post(self.register_url, {
            'register-name': 'A',
            'register-email': 'shortname@test.com',
            'register-password': 'Test123!',
            'register-confirm': 'Test123!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='shortname@test.com').exists())
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any('nome completo' in str(msg).lower() for msg in messages_list))

    def test_valid_registration(self):
        """Test 10: Verifica che la registrazione valida crei un utente"""
        response = self.client.post(self.register_url, {
            'register-name': 'Test User',
            'register-email': 'valido@test.com',
            'register-password': 'Test123!',
            'register-confirm': 'Test123!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email='valido@test.com').exists())
        user = User.objects.get(email='valido@test.com')
        self.assertEqual(user.full_name, 'Test User')
        self.assertTrue(user.check_password('Test123!'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertTrue(any('registrazione completata' in str(msg).lower() for msg in messages_list))

#test funzionalità di view profilo utente + codice di risposta HTTP
    def test_profile_view(self):
        """Test 11: Verifica la vista del profilo utente"""
        user = User.objects.create_user(
            email='profile@test.com',
            password='Test123!',
            full_name='Profile User'
        )
        self.client.login(email='profile@test.com', password='Test123!')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile User')
        self.assertContains(response, 'profile@test.com')
