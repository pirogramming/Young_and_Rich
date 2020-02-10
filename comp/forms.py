from django import forms

from comp.models import ComPost, ComComment, Answer


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
        fields = ['comp', 'user', 'file', 'rank', 'accuracy']
        widgets = {

            'comp': forms.HiddenInput,
            'user': forms.HiddenInput,
            'rank': forms.HiddenInput,
            'accuracy': forms.HiddenInput,
        }