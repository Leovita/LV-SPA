from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import SubscriptionPlan
from django.contrib.auth.decorators import login_required

@login_required
def subscription_plans(request):
    """View to display all available subscription plans"""
    subscription_plans = SubscriptionPlan.objects.all()
    context = {
        'subscription_plans': subscription_plans
    }
    return render(request, 'subscriptions/subscription.html', context)

@login_required
def subscribe_plan(request, plan_id):
    """View to subscribe to a specific plan"""
    if request.method == 'POST':
        plan = get_object_or_404(SubscriptionPlan, id=plan_id)
        
        user = request.user
        user.plan = plan
        user.subscription = f"{plan.name} ({plan.duration} giorni)"
        user.save()
        
        messages.success(request, f"Abbonamento '{plan.name}' sottoscritto con successo!")
        return redirect('subscription_plans')
    
    return redirect('subscription_plans')