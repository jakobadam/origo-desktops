from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, path):
    request_path = context['request'].path
    if path in request_path:
        return 'active'
    return ''

