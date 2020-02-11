from django import forms
from django.contrib.admin import widgets

from comp.models import ComPost, ComComment, Answer, Comp


class ComPostForm(forms.ModelForm):
    class Meta:
        model = ComPost
        fields = ("title", "context",)


class ComCommentForm(forms.ModelForm):
    class Meta:
        model = ComComment
        fields = ("context",)

# from .models import Answer

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [ 'comp','user', 'file', 'rank','accuracy']
        widgets = {

            'comp':forms.HiddenInput,
            'user': forms.HiddenInput,
            'rank': forms.HiddenInput,
            'accuracy': forms.HiddenInput,
        }


class CompForm(forms.ModelForm):
    class Meta:
        model=Comp
        fields = ['title', 'context','profile_thumb', 'back_thumb', 'prize', 'deadline', 'evaluation','overview_context', 'data_context','answer',]
        widgets = {
            'deadline': widgets.AdminSplitDateTime,
        }

class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))