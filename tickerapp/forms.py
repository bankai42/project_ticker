from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class TickerTextForm(forms.Form):
    text = forms.CharField(label='Enter text for a ticker', max_length=255)
    filename = forms.CharField(label='Enter name for a ticker file', max_length=255)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']