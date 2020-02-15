from django.contrib import admin

from comp.models import Comp, ComPost, ComComment, Answer

admin.site.register(Comp)
admin.site.register(ComPost)
admin.site.register(ComComment)
admin.site.register(Answer)