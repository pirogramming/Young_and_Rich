from django.contrib import admin

from comp.models import Comp, ComPost, ComComment

admin.site.register(Comp)
admin.site.register(ComPost)
admin.site.register(ComComment)
