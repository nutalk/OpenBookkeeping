prop_type_items = ['Capital Assets', 'Liquid Assets', 'Long-term Liabilities', 'Current Liability']

prop_type_ids = {item: idx for idx, item in enumerate(prop_type_items)}

liability_currency_types = ['No', 'Fixed-payment ', 'Interest-first', 'Fixed-principal', 'Upon maturity']

liability_currency_ids = {item: idx for idx, item in enumerate(liability_currency_types)}

account_info_show = {
    'name': 'Account Name',
    'p_type': 'Account Type',
    'start_date': 'Start Date',
    'term_month': 'Terms',
    'rate': 'Interest Rate',
    'currency': 'Cash Flow',
    'ctype': 'Repayment',
    'comment': 'Comment'
}

history_month_term = 24
predict_month_term = 24