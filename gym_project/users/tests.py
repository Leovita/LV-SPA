from django.test import TestCase
from .models import User
from subscriptions.models import SubscriptionPlan, Subscription
from spa.models import SpaService

class StaffSubscriptionTests(TestCase):
    def setUp(self):
        self.annual_plan = SubscriptionPlan.objects.create(
            id=3,
            name="Annual Plan",
            price=100,
            duration=12
        )
        
        self.staff_user = User.objects.create_user(
            email='staff@example.com',
            password='Staff123!@#',
            full_name='Staff User',
            is_staff=True
        )
        
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='Admin123!@#'
        )
        
        self.normal_user = User.objects.create_user(
            email='normal@example.com',
            password='Normal123!@#',
            full_name='Normal User'
        )

    def test_staff_sub(self):
        staff_subscription = Subscription.objects.filter(
            user=self.staff_user,
            plan=self.annual_plan,
            is_active=True
        ).first()
        
        self.assertIsNotNone(staff_subscription, "Lo staff dovrebbe avere un abbonamento attivo")
        self.assertEqual(staff_subscription.plan, self.annual_plan, "L'abbonamento dovrebbe essere annuale")

    def test_admin_sub(self):
        admin_subscription = Subscription.objects.filter(
            user=self.admin_user,
            plan=self.annual_plan,
            is_active=True
        ).first()
        
        self.assertIsNotNone(admin_subscription, "L'admin dovrebbe avere un abbonamento attivo")
        self.assertEqual(admin_subscription.plan, self.annual_plan, "L'abbonamento dovrebbe essere annuale")

    def test_normal_user_no_subscription(self):
        #testiamo che un utente normale non abbia un abbonamento attivo default
        normal_subscription = Subscription.objects.filter(
            user=self.normal_user,
            plan=self.annual_plan,
            is_active=True
        ).first()
        
        self.assertIsNone(normal_subscription, "Un utente normale non dovrebbe avere un abbonamento automatico")

    def test_staff_to_normal_user_subscription(self):
        #rimuoviamo i privilegi staff e vediamo se l'abbonamento viene rimosso
        self.staff_user.is_staff = False
        self.staff_user.save()
        
        staff_subscription = Subscription.objects.filter(
            user=self.staff_user,
            plan=self.annual_plan,
            is_active=True
        ).first()
        
        self.assertIsNotNone(staff_subscription, "L'abbonamento dovrebbe essere mantenuto anche dopo la rimozione dei privilegi staff")

    def test_multiple_staff_subscriptions(self):
        #salviamo nuovamente l'utente staff per forzare il trigger
        self.staff_user.save()
        
        #count sub attivi
        subscription_count = Subscription.objects.filter(
            user=self.staff_user,
            plan=self.annual_plan,
            is_active=True
        ).count()
        
        self.assertEqual(subscription_count, 1, "Dovrebbe esserci un solo abbonamento attivo")

    def test_subscription_after_staff_promotion(self):
        #promuoviamo l'utente normale a staff
        self.normal_user.is_staff = True
        self.normal_user.save()
        
        #testiamo che l'utente abbia ricevuto l'abbonamento
        normal_user_subscription = Subscription.objects.filter(
            user=self.normal_user,
            plan=self.annual_plan,
            is_active=True
        ).first()
        
        self.assertIsNotNone(normal_user_subscription, "User promosso a staff non ha subsciption")
        self.assertEqual(normal_user_subscription.plan, self.annual_plan, "L'abbonamento dovrebbe essere annuale")

class SpaServicePriceTests(TestCase):
    def setUp(self):
        self.plan = SubscriptionPlan.objects.create(
            name="Abbonamento Annuale",
            price=279.99,
            duration=12,
            description="Il miglior rapporto qualità-prezzo! 12 mesi di benessere totale"
        )
        
        self.user = User.objects.create_user(
            email='user@example.com',
            password='User123!@#',
            full_name='Normal User'
        )
        
        self.spa_service = SpaService.objects.create(
            name="Massaggio Relax",
            description="Massaggio rilassante di 45 minuti",
            price=50,
            duration=45,
            max_partecipants=1
        )

    def test_spa_service_price_with_subscription(self):
        # Verifico che inizialmente l'utente non abbia accesso gratuito
        self.assertFalse(self.user.has_free_spa_access())
        
        # Creo un abbonamento attivo per l'utente
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            is_active=True
        )
        
        self.assertTrue(self.user.has_free_spa_access())
        self.assertEqual(self.spa_service.get_price_for_user(self.user), 0)

    def test_spa_service_price_without_subscription(self):
        self.assertEqual(self.spa_service.get_price_for_user(self.user), self.spa_service.price)
