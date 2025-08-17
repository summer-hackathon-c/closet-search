from django import template

register = template.Library()


@register.filter
def yen(value):
    try:
        return f"{int(value):,}円"
    except (TypeError, ValueError):
        return value
