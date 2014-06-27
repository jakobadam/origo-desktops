from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, path):
    request_path = context['request'].path
    if request_path == path:
        return 'active'
    return ''
