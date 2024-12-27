from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import AppendedText
from crispy_forms.layout import Submit, Layout, Field
from .gloab_info import prop_type_items, liability_currency_types
from django.utils.translation import get_language, gettext_lazy as _


class PropNewForm(forms.Form):
    id = forms.IntegerField(label='id')
    name = forms.CharField(label=_('Account Name'), max_length=255, required=True)
    p_type = forms.ChoiceField(choices=[(idx, _(item)) for idx, item in enumerate(prop_type_items)], 
                                  required=True, label=_('Account Type'))
    start_date = forms.DateField(required=True, label=_('Start Date'),
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    term_month = forms.IntegerField(required=True, initial=0, label=_('Terms'))
    rate = forms.FloatField(required=True, initial=0.0, label=_('Interest Rate'))
    currency = forms.IntegerField(required=True, initial=0, label=_('Cash Flow'))
    ctype = forms.ChoiceField(choices=[(idx, _(item)) for idx, item in enumerate(liability_currency_types)], 
                              required=True, label=_('Repayment'))
    comment = forms.CharField(label=_('Comment'), max_length=255, required=False)
    init_ammount = forms.IntegerField(required=True, initial=0, label=_('Init Balance'))

    def __init__(self, action_str, form_id: str, form_class: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_language = get_language()
        out = _('Init Balance')
        # iout = _('Interest Rate')
        print(f"{user_language=}, {out=}")
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
            AppendedText('term_month', _('month'), active=False),
            AppendedText('rate', '%', active=False),
            'currency',
            'ctype',
            'comment',
            AppendedText('init_ammount', _('$'), active=False)
        )

        self.helper.add_input(Submit('submit', _('Submit')))


class PropEditForm(forms.Form):
    id = forms.IntegerField(label='id')
    name = forms.CharField(label=_('Account Name'), max_length=255, required=True)
    p_type = forms.ChoiceField(choices=[(idx, item) for idx, item in enumerate(prop_type_items)], 
                                  required=True, label=_('Account Type'))
    start_date = forms.DateField(required=True, label=_('Start Date'),
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    term_month = forms.IntegerField(required=True, initial=0, label=_('Terms'))
    rate = forms.FloatField(required=True, initial=0.0, label=_('Interest Rate'))
    currency = forms.IntegerField(required=True, initial=0, label=_('Cash Flow'))
    ctype = forms.ChoiceField(choices=[(idx, item) for idx, item in enumerate(liability_currency_types)], 
                              required=True, label=_('Repayment'))
    comment = forms.CharField(label=_('Comment'), max_length=255, required=False)

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
            AppendedText('term_month', _('month'), active=False),
            AppendedText('rate', '%', active=False),
            'currency',
            'ctype',
            'comment'
        )
        self.helper.add_input(Submit('submit', _('Submit')))


class DetailForm(forms.Form):
    id = forms.IntegerField(label='id')
    target_id = forms.ImageField(label='tid')
    occur_date = forms.DateField(required=True, label=_('Date'),
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    amount = forms.IntegerField(label=_('amount'), required=True, initial=0)
    comment = forms.CharField(label=_('Comment'), max_length=255, required=False)

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
            AppendedText('amount', _('$'), active=False),
            'comment'
        )

        self.helper.add_input(Submit('submit', _('Submit')))

