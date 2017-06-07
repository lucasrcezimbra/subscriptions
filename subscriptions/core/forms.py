from django import forms
from subscriptions.core.models import Subscription

class ExportForm(forms.Form):
    FORMATS = (('csv', 'CSV'), )
    FIELDS = [(field.name, field.verbose_name)
              for field in Subscription._meta.get_fields()]
    format = forms.ChoiceField(label='Formato', widget=forms.RadioSelect,
                               choices=FORMATS)
    fields = forms.MultipleChoiceField(label='Campos', choices=FIELDS)
