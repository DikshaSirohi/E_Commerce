from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def calculate_item_total(item):
    """Calculate total cost for a cart item"""
    return item.get_total_price()
