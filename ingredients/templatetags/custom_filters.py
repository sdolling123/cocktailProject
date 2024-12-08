from django import template

register = template.Library()

@register.filter
def get_value_from_checkbox(value):
    """
    Extracts the numeric ID from a checkbox input value.
    Assumes the value format is something like 'field_name-value'.
    """
    try:
        return int(value.split('-')[-1])
    except (ValueError, IndexError):
        return None
    
@register.filter(name='replace_underscore')
def replace_underscore(value):
    """Replace underscores with spaces"""
    return value.replace('_', ' ')

@register.filter
def get_item(dictionary, key):
    return dictionary[key]