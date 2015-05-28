from django.template import Variable, VariableDoesNotExist
from django import template
from django.template import Variable, VariableDoesNotExist

register = template.Library()

@register.filter
def hash(object, attr):
    pseudo_context = { 'object' : object }
    try:
        value = Variable('object.%s' % attr).resolve(pseudo_context)
    except VariableDoesNotExist:
        value = None
    return value

@register.filter
def resolve(lookup, target):
    try:
        return lookup[target]
    except Exception as e:
        print e
        return None

@register.filter(name='replace')
def replace(object, s):
    return str(object).replace(s,'')

@register.filter(name='get_class')
def get_class(value):
  return value.__class__.__name__


@register.filter(name='sort')
def sort(list):
  return sorted(list)
