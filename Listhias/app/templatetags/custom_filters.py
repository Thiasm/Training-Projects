from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    if isinstance(value, str):
        return value.split(delimiter)
    return value
