from django import template

register = template.Library()

@register.filter
def truncate_description(description, max_length):
    if len(description) > max_length:
        return description[:max_length] + "..."
    return description