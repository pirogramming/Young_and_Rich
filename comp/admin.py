from django.contrib import admin

from comp.models import Comp, ComPost, ComComment, CodePost, CodeComment, Answer

admin.site.register(Comp)
admin.site.register(CodePost)
admin.site.register(CodeComment)
admin.site.register(ComPost)
admin.site.register(ComComment)
admin.site.register(Answer)
