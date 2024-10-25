from django import template

register = template.Library()


@register.filter
def background_color(value):
    if value > 0:
        return f'rgba(0, 255, 0, {min(value * 0.25, 1)})'  # green color
    elif value < 0:
        return f'rgba(255, 0, 0, {min((-value) * 0.25, 1)})'  # red color
    return 'rgba(255, 255, 255, 1)'  # white or neutral color
