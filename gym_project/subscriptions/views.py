from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Subscription, SubscriptionPlan
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.utils import timezone
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

def validate_fake_card_data(view_func):
    def _wrapped_view(request, plan_id, *args, **kwargs):
        if request.method == 'POST':
            card_name = request.POST.get('card_name', '').strip()
            card_number = request.POST.get('card_number', '').replace(' ', '')
            card_expiry = request.POST.get('card_expiry', '').strip()
            card_cvv = request.POST.get('card_cvv', '').strip()
            errors = []
            if not card_name or len(card_name.split()) < 2:
                errors.append('Inserisci il nome completo come sulla carta.')
            if not card_number.isdigit() or len(card_number) != 16:
                errors.append('Il numero della carta deve essere di 16 cifre.')
            if not re.match(r'^(0[1-9]|1[0-2])\/\d{2}$', card_expiry):
                errors.append('La scadenza deve essere nel formato MM/AA.')
            else:
                # controllo che non sia scaduta
                try:
                    exp_month, exp_year = card_expiry.split('/')
                    exp_month = int(exp_month)
                    exp_year = int('20' + exp_year) if len(exp_year) == 2 else int(exp_year)
                    now = datetime.now()
                    if exp_year < now.year or (exp_year == now.year and exp_month < now.month):
                        errors.append('La carta è scaduta. Inserisci una data valida.')
                except Exception:
                    errors.append('Data di scadenza non valida.')
            if not card_cvv.isdigit() or len(card_cvv) != 3:
                errors.append('Il CVV deve essere di 3 cifre.')
            if errors:
                for err in errors:
                    messages.error(request, err)
                return redirect('subscription_plans')
        return view_func(request, plan_id, *args, **kwargs)
    return _wrapped_view

@login_required
def subscription_plans(request):
    """View to display all available subscription plans"""
    plans = SubscriptionPlan.objects.all()
    context = {
        "subscription_plans": plans,
        "user_subscription": Subscription.objects.filter(user=request.user, is_active=True).first(),
    }
    return render(request, 'subscriptions/subscription.html', context)

@login_required
@validate_fake_card_data
def subscribe_plan(request, plan_id):
    """View to subscribe to a specific plan and link it to the user"""
    if request.method == 'POST':
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)
        Subscription.objects.filter(user=request.user, is_active=True).update(is_active=False)
        card_name = request.POST.get('card_name')
        card_number = request.POST.get('card_number')
        card_expiry = request.POST.get('card_expiry')
        card_cvv = request.POST.get('card_cvv')
        
        start_date = timezone.now()
        end_date = start_date + relativedelta(months=plan.duration)
        
        subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            is_active=True
        )
        messages.success(request, f"Abbonamento '{plan.name}' sottoscritto con successo!")
        return redirect('subscription_plans')
    return redirect('subscription_plans')