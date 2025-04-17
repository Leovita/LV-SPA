from django import template

register = template.Library()

# filtro custom per recuperare dal dizionario delle date il valore in base al service.id 
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)