from django import forms
from .models import Poll, Choice
from django.forms import inlineformset_factory

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'})
        }

ChoiceFormSet = inlineformset_factory(Poll, Choice, fields=['choice_text'], extra=2, can_delete=False,
    widgets={'choice_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter choice'})},
    labels={'choice_text': 'Choice'})