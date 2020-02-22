from django import forms
from django.contrib.admin import widgets

from comp.models import ComPost, ComComment, Answer, Comp, CodePost, CodeComment


class ComPostForm(forms.ModelForm):
    class Meta:
        model = ComPost
        fields = ("title", "context",)

    title = forms.CharField(label='제목', widget=forms.TextInput(
        attrs={
            'class': 'form-control input-lg',
            'placeholder': '제목 여기!'
        }))

    context = forms.CharField(label='내용', widget=forms.Textarea(
        attrs={
            'class': 'form-control input-lg',
            'placeholder': '내용 여기!'
        }))


class CodePostForm(forms.ModelForm):
    class Meta:
        model = CodePost
        fields = ("title", "context_code", "context")

    title = forms.CharField(label='제목', widget=forms.TextInput(
        attrs={
            'class': 'form-control input-lg',
            'placeholder': ''
        }))

    context_code = forms.CharField(label='코드', widget=forms.Textarea(
        attrs={
            'class': 'form-control input-lg',
            'placeholder': '코드를 작성하세요'
        }))

    context = forms.CharField(label='코드설명', widget=forms.Textarea(
        attrs={
            'class': 'form-control input-lg',
            'placeholder': '코드 설명을 작성하세요'
        }))



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
