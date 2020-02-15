from django.contrib import admin

from comp.models import Comp, ComPost, ComComment, CodePost, CodeComment

admin.site.register(Comp)
admin.site.register(CodePost)
admin.site.register(CodeComment)
admin.site.register(ComPost)
admin.site.register(ComComment)
