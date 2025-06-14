from django.db import migrations

def convert_days_to_months(apps, schema_editor):
    SubscriptionPlan = apps.get_model('subscriptions', 'SubscriptionPlan')
    # Aggiorna i piani esistenti con i valori corretti in mesi
    plans = {
        'Piano Base': 3,  # 3 mesi
        'Piano Premium': 6,  # 6 mesi
        'Piano VIP': 12,  # 12 mesi
    }
    for plan in SubscriptionPlan.objects.all():
        if plan.name in plans:
            plan.duration = plans[plan.name]
            plan.save()

class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_subscription'),
    ]

    operations = [
        migrations.RunPython(convert_days_to_months),
    ] 