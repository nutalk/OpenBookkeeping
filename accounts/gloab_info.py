prop_type_items = ['固定资产', '流动资产', '长期负债', '短期负债']

prop_type_ids = {item: idx for idx, item in enumerate(prop_type_items)}

liability_currency_types = ['无', '等额本息', '先息后本', '等额本金', '到期还本付息']

liability_currency_ids = {item: idx for idx, item in enumerate(liability_currency_types)}

account_info_show = {
    'name': '名称',
    'p_type': '类型',
    'start_date': '开始日期',
    'term_month': '期数',
    'rate': '年利率',
    'currency': '现金流',
    'ctype': '还款方式',
    'comment': '备注'
}

history_month_term = 24
predict_month_term = 24