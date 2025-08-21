from django import template

register = template.Library()


@register.filter
def to_yen(value):
    try:
        return f"{int(value):,}円"
    except (TypeError, ValueError):
        return value
