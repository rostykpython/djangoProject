from django import forms
from datetime import datetime


CHOICES_TYPE = (
    ('1', 'Income'),
    ('2', 'Expenditures')
)


class SubmitForm(forms.Form):
    type = forms.ChoiceField(choices=CHOICES_TYPE, label='Type of money')


class IncomeForm(forms.Form):
    category = forms.CharField(max_length=200)
    name = forms.CharField()
    value = forms.IntegerField(min_value=0)
    date_added = forms.DateTimeField(
        widget=forms.SelectDateWidget(years=[year for year in range(2010, datetime.now().year + 1)])
    )
    is_periodical = forms.BooleanField(required=False)


class ExpenditureForm(forms.Form):
    category = forms.CharField(max_length=200)
    name = forms.CharField(max_length=200)
    value = forms.IntegerField()
    date_added = forms.DateTimeField(widget=forms.SelectDateWidget())

