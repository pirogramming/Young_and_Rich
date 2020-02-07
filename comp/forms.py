from django import forms

from .models import Answer


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [ 'comp','user', 'file', 'nth_submit', 'rank','accuracy']
        widgets = {

            'comp':forms.HiddenInput,
            'nth_submit': forms.HiddenInput,
            'user': forms.HiddenInput,
            'rank': forms.HiddenInput,
            'accuracy': forms.HiddenInput,
        }