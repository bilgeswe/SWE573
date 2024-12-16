from django import template

# Create template library instance
register = template.Library()


@register.filter(name='add_class')
def add_class(value, css_class):
    """Add CSS class to form field widget"""
    return value.as_widget(attrs={'class': css_class})
