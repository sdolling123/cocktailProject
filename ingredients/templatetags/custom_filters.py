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
    proper_formatting = value.title()
    return proper_formatting.replace('_', ' ')

@register.filter
def get_item(dictionary, key):
    return dictionary[key]

@register.filter
def get_abbreviated_unit(cocktail_ingredient):
    return cocktail_ingredient.get_abbreviated_unit()

@register.filter
def format_number(value):
    """
    Removes '.0' from whole numbers, otherwise returns the original number.
    """
    try:
        # Check if value is numeric
        if isinstance(value, (int, float)) and value == int(value):
            return int(value)  # Return as integer if it's a whole number
        return value  # Return original value otherwise
    except (ValueError, TypeError):
        return value  # In case of error, return original value
    
@register.filter
def extract_suffix(value):
    """
    Extracts the string after the second underscore in the input string.
    Example:
        Input: "ingredient_id_9762d864c39e46cdb41f5ee492d92ef3"
        Output: "9762d864c39e46cdb41f5ee492d92ef3"
    """
    if not isinstance(value, str):
        return value
    parts = value.split("_", 2)
    return parts[2] if len(parts) > 2 else ""