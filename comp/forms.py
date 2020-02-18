from django import forms
from django.contrib.admin import widgets

from comp.models import ComPost, ComComment, Answer, Comp, CodePost, CodeComment


class ComPostForm(forms.ModelForm):
    class Meta:
        model = ComPost
        fields = ("title", "context",)


class CodePostForm(forms.ModelForm):
    class Meta:
        model = CodePost
        fields = ("title", "context",)


class ComCommentForm(forms.ModelForm):
    class Meta:
        model = ComComment
        fields = ("context",)


class CodeCommentForm(forms.ModelForm):
    class Meta:
        model = CodeComment
        fields = ("context",)


# from .models import Answer



class CompForm(forms.ModelForm):
    class Meta:
        model = Comp
        fields = ['title', 'context', 'profile_thumb', 'back_thumb', 'prize', 'deadline', 'evaluation',
                  'overview_context', 'data_context', 'comp_answer', ]
        widgets = {
            'deadline': widgets.AdminSplitDateTime,
        }


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
