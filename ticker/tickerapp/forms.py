from django import forms

class TickerTextForm(forms.Form):
    text = forms.CharField(label='Enter text for a ticker', max_length=255)