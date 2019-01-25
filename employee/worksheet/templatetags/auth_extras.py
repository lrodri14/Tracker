from django import template
from django.contrib.auth.models import Permission

register = template.Library()

@register.filter(name='has_permiso')
def has_permiso(user, permiso_name):
    if user.user_permissions.filter(codename=permiso_name).exists():
        return True
    return False
