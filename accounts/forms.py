from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import AppendedText
from crispy_forms.layout import Submit, Layout, Field
from .gloab_info import prop_type_ids, prop_type_items, \
    liability_currency_ids, liability_currency_types, account_info_show


class PropNewForm(forms.Form):
    id = forms.IntegerField(label='id')
    name = forms.CharField(label='账户名称', max_length=255, required=True)
    p_type = forms.ChoiceField(choices=[(idx, item) for idx, item in enumerate(prop_type_items)], 
                                  required=True, label='账户类型')
    start_date = forms.DateField(required=True, label='开始日期',
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    term_month = forms.IntegerField(required=True, initial=0, label='期数')
    rate = forms.FloatField(required=True, initial=0.0, label='年利率')
    currency = forms.IntegerField(required=True, initial=0, label='现金流')
    ctype = forms.ChoiceField(choices=[(idx, item) for idx, item in enumerate(liability_currency_types)], 
                              required=True, label='还款方式')
    comment = forms.CharField(label='备注', max_length=255, required=False)
    init_ammount = forms.IntegerField(required=True, initial=0, label='初始金额')

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
            AppendedText('term_month', '月', active=False),
            AppendedText('rate', '%', active=False),
            'currency',
            'ctype',
            'comment',
            AppendedText('init_ammount', '元', active=False)
        )

        self.helper.add_input(Submit('submit', '提交'))


class DetailForm(forms.Form):
    id = forms.IntegerField(label='id')
    target_id = forms.ImageField(label='tid')
    occur_date = forms.DateField(required=True, label='日期',
                                 widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    amount = forms.IntegerField(label='金额', required=True, initial=0)
    comment = forms.CharField(label='备注', max_length=255, required=False)

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
            AppendedText('amount', '元', active=False),
            'comment'
        )

        self.helper.add_input(Submit('submit', '提交'))

