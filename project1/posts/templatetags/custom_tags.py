from django import template

register = template.Library()

@register.filter
def index(sequence, position):
    print(type(sequence))
    print(type(position))
    return sequence[position]
