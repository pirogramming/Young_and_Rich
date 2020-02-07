from django import forms

from comp.models import ComPost, ComComment


class ComPostForm(forms.ModelForm):

    class Meta:
        model = ComPost
        fields = ("title", "context",)


class ComCommentForm(forms.ModelForm):

    class Meta:
        model = ComComment
        fields = ("context",)
