from django.contrib import admin

from comp.models import Comp, ComPost, ComComment, CodeComment, CodePost

admin.site.register(Comp)
admin.site.register(ComPost)
admin.site.register(ComComment)
admin.site.register(CodeComment)
admin.site.register(CodePost)