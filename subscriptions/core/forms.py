from django import forms

class SubscriptionForm(forms.Form):
    file = forms.FileField(label='Arquivo')
