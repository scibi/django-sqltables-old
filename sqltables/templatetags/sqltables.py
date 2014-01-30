from django import template

register = template.Library()

@register.inclusion_tag('sqltables/css.html')
def sqltables_css():
    pass

@register.inclusion_tag('sqltables/js.html')
def sqltables_js():
    pass
