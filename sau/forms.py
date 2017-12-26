from django import forms

from .models import Sheep, Dose


class DateInput(forms.DateInput):
    input_type = 'date'


class DoseForm(forms.ModelForm):
    class Meta:
        model = Dose
        fields = ('medicine', 'amount', 'date_utc')
        widgets = {'date_utc': DateInput()}


class SheepForm(forms.ModelForm):
    class Meta:
        model = Sheep
        fields = ('name', 'ear_tag', 'ear_tag_color', 'birth_date_utc',
                  'sex', 'mother', 'father', 'origin')

        widgets = {
            'date_utc': DateInput(),
            'origin': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['father'].queryset = Sheep.objects.filter(sex='m')  # male
        self.fields['mother'].queryset = Sheep.objects.filter(sex='f')  # female
