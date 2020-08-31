from django import template

register = template.Library()

@register.filter
def keyvalue(dict, key):
    try:
        return dict[key]
    except KeyError:
        return ''

@register.filter
def resultcount(dict):
    try:
        return dict['result_count']
    except KeyError:
        return ''
