from django import forms


CHOICES_TYPE = (
    ('1', 'Income'),
    ('2', 'Expenditures')
)


class SubmitForm(forms.Form):
    type = forms.ChoiceField(choices=CHOICES_TYPE, label='Type of money')


class IncomeForm(forms.Form):
    category = forms.CharField(max_length=200, required=False)
    name = forms.CharField(required=False)
    value = forms.IntegerField(min_value=0, required=False)
    date_added = forms.DateField(
        widget=forms.SelectDateWidget()
    )
    is_periodical = forms.BooleanField(required=False)


class ExpenditureForm(forms.Form):
    category = forms.CharField(max_length=200, required=False)
    name = forms.CharField(max_length=200, required=False)
    value = forms.IntegerField(required=False)
    date_added = forms.DateField(
        widget=forms.SelectDateWidget()
    )


class ReportForm(forms.Form):
    date_from = forms.DateField(
        widget=forms.SelectDateWidget()
    )
    date_to = forms.DateField(
        widget=forms.SelectDateWidget()
    )
