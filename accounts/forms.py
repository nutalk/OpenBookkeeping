from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import AppendedText
from crispy_forms.layout import Submit, Layout, Field
from .gloab_info import prop_type_items, liability_currency_types
from django.utils.translation import gettext_lazy as lazy


class PropNewForm(forms.Form):
    id = forms.IntegerField(label='id')
    name = forms.CharField(label=lazy('Account Name'), max_length=255, required=True)
    p_type = forms.ChoiceField(choices=[(idx, item) for idx, item in enumerate(prop_type_items)], 
                                  required=True, label=lazy('Account Type'))
    start_date = forms.DateField(required=True, label=lazy('Start Date'),
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    term_month = forms.IntegerField(required=True, initial=0, label=lazy('Terms'))
    rate = forms.FloatField(required=True, initial=0.0, label=lazy('Interest Rate'))
    currency = forms.IntegerField(required=True, initial=0, label=lazy('Cash Flow'))
    ctype = forms.ChoiceField(choices=[(idx, item) for idx, item in enumerate(liability_currency_types)], 
                              required=True, label=lazy('Repayment'))
    comment = forms.CharField(label=lazy('Comment'), max_length=255, required=False)
    init_ammount = forms.IntegerField(required=True, initial=0, label=lazy('Init Balance'))

    def __init__(self, action_str, form_id: str, form_class: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = form_id
        self.helper.form_class = form_class
        self.helper.form_method = 'post'
        self.helper.form_action = action_str
        self.helper.layout = Layout(
            Field('id', type='hidden'),
            'name',
            'p_type',
            'start_date',
            AppendedText('term_month', lazy('month'), active=False),
            AppendedText('rate', '%', active=False),
            'currency',
            'ctype',
            'comment',
            AppendedText('init_ammount', lazy('$'), active=False)
        )

        self.helper.add_input(Submit('submit', lazy('Submit')))


class PropEditForm(forms.Form):
    id = forms.IntegerField(label='id')
    name = forms.CharField(label=lazy('Account Name'), max_length=255, required=True)
    p_type = forms.ChoiceField(choices=[(idx, item) for idx, item in enumerate(prop_type_items)], 
                                  required=True, label=lazy('Account Type'))
    start_date = forms.DateField(required=True, label=lazy('Start Date'),
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    term_month = forms.IntegerField(required=True, initial=0, label=lazy('Terms'))
    rate = forms.FloatField(required=True, initial=0.0, label=lazy('Interest Rate'))
    currency = forms.IntegerField(required=True, initial=0, label=lazy('Cash Flow'))
    ctype = forms.ChoiceField(choices=[(idx, item) for idx, item in enumerate(liability_currency_types)], 
                              required=True, label=lazy('Repayment'))
    comment = forms.CharField(label=lazy('Comment'), max_length=255, required=False)

    def __init__(self, action_str, form_id: str, form_class: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = form_id
        self.helper.form_class = form_class
        self.helper.form_method = 'post'
        self.helper.form_action = action_str
        self.helper.layout = Layout(
            Field('id', type='hidden'),
            'name',
            'p_type',
            'start_date',
            AppendedText('term_month', lazy('month'), active=False),
            AppendedText('rate', '%', active=False),
            'currency',
            'ctype',
            'comment'
        )
        self.helper.add_input(Submit('submit', lazy('Submit')))


class DetailForm(forms.Form):
    id = forms.IntegerField(label='id')
    target_id = forms.ImageField(label='tid')
    occur_date = forms.DateField(required=True, label=lazy('Date'),
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    amount = forms.IntegerField(label=lazy('amount'), required=True, initial=0)
    comment = forms.CharField(label=lazy('Comment'), max_length=255, required=False)

    def __init__(self, action_str, form_id: str, form_class: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = form_id
        self.helper.form_class = form_class
        self.helper.form_method = 'post'
        self.helper.form_action = action_str
        self.helper.layout = Layout(
            Field('id', type='hidden'),
            Field('target_id', type='hidden'),
            'occur_date',
            AppendedText('amount', lazy('$'), active=False),
            'comment'
        )

        self.helper.add_input(Submit('submit', lazy('Submit')))

