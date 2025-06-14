from django import template
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def is_future(value):
    if isinstance(value, datetime):
        return value > timezone.now()
    return False

@register.filter
def format_datetime(value):
    if isinstance(value, datetime):
        return value.strftime('%d/%m/%Y %H:%M')
    return value 