import os

from django import template


register = template.Library()

@register.filter
def filename(self):
    return os.path.basename(self.file.name)[2:]