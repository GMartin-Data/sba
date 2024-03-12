from django import forms

from .models import LoanApplication


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        exclude = ['Region', 'SameState', 'Recession', 'Verdict', 'Percentage']
        integer_field_name = forms.IntegerField(min_value=0)

    def __init__(self, *args, **kwargs):
        super(LoanApplicationForm, self).__init__(*args, **kwargs)
        # Définir des widgets personnalisés pour chaque champ
        for field_name in self.fields:
            if isinstance(self.fields[field_name], forms.CharField):
                self.fields[field_name].widget = forms.TextInput(
                    attrs={'class': 'focus:border-text-sba-dark-blue focus:outline-none focus:ring-1 focus:ring-text-sba-dark-blue'})
            elif isinstance(self.fields[field_name], forms.FloatField):
                self.fields[field_name].widget = forms.NumberInput(
                    attrs={'class': 'focus:border-text-sba-dark-blue focus:outline-none focus:ring-1 focus:ring-text-sba-dark-blue', 'min': 0})
            elif isinstance(self.fields[field_name], forms.IntegerField):
                self.fields[field_name].widget = forms.NumberInput(
                    attrs={'class': 'focus:border-text-sba-dark-blue focus:outline-none focus:ring-1 focus:ring-text-sba-dark-blue', 'min': 0})
