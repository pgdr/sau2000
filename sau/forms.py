from django import forms
from .models import Sheep, Dose


class DateInput(forms.DateInput):
    input_type = 'date'


class DoseForm(forms.ModelForm):
    class Meta:
        model = Dose
        fields = ('medicine', 'amount', 'date_utc')
        widgets = {'date_utc': DateInput()}
