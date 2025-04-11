from django import forms
from .models import Poll, Choice
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'