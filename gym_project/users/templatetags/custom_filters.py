from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    value = dictionary.get(key)
    return value if value is not None else '' 