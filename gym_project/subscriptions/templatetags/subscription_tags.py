from django import template

register = template.Library()

@register.filter
def to_months(days):
    """Convert days to months (assuming 30 days per month)"""
    months = days // 30
    if months > 0:
        return f"{months} mesi"
    return f"{days} giorni" 