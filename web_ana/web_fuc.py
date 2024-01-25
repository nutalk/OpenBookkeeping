import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import json
import pandas as pd
from loguru import logger
import csv
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

from OpenBookkeeping.sql_db import query_by_col, update_by_col, add_detail, del_by_col, query_table, query_by_str
from OpenBookkeeping.cash_flow import EqualDelt, InterestLoan, FinishLoan, EqualPrincipalPayment
from OpenBookkeeping.gloab_info import prop_type_items, liability_currency_types


prop_query_str = """
select type, name, start_date, term_month, rate, currency, ctype, sum(amount) from prop 
LEFT outer join prop_details
on prop.id = prop_details.target_id group by name;
"""


def get_prop_data(db_path: str):
    props = query_by_str(db_path, prop_query_str)
    prop_df = pd.DataFrame(props, columns=['type', 'name', 'start_date', 'term_month', 'rate', 'currency', 'ctype',
                                           'sum_amount'])
    prop_df.fillna(0, inplace=True)
    prop_df['type_cn'] = prop_df['type'].apply(lambda x: prop_type_items[x])
    return prop_df


def get_amount(prop_df: pd.DataFrame) -> dict:
    as_amount = np.sum(prop_df[prop_df['type'] <= 1]['sum_amount'])
    de_amount = np.sum(prop_df[prop_df['type'] >= 2]['sum_amount'])
    ne_amount = as_amount - de_amount
    cash = np.sum(prop_df[prop_df['type'] == 1]['sum_amount'])
    return {'as': round(as_amount / 10000), 'de': round(de_amount / 10000),
            'ne': round(ne_amount / 10000), 'cash': round(cash / 10000, 2)}


detail_str = """
select type, name, occur_date, amount 
from prop LEFT outer join prop_details on prop.id = prop_details.target_id;
"""


def get_month_history_data(db_path: str, history_month_term: int) -> pd.DataFrame:
    """
    获取历史各月的资产、负债与净资产数据
    :param db_path:
    :param history_month_term:
    :return:
    """
    prop_details = query_by_str(db_path, detail_str)
    prop_detail_df = pd.DataFrame(prop_details, columns=['type', 'name', 'occur_date', 'amount'])
    prop_detail_df.dropna(inplace=True)

    prop_detail_df['o_date'] = prop_detail_df['occur_date'].apply(lambda \
          x: datetime.strptime(x, '%Y-%m-%d').date())

    td = relativedelta(months=1, day=1)
    next_month_first_day = datetime.today().date() + td

    per_month_rec = []
    for i in range(0-history_month_term, 1, 1):
        end_date = next_month_first_day + relativedelta(months=i, day=1)
        end_df = prop_detail_df[prop_detail_df['o_date'] < end_date]
        prop_sum = np.sum(end_df[end_df['type'] <= 1]['amount'])
        det_sum = np.sum(end_df[end_df['type'] > 1]['amount'])
        net_sum = prop_sum - det_sum
        per_month_rec.append(
            {'日期': end_date, '资产(万)': round(prop_sum / 10000), '负债(万)': round(det_sum / 10000),
             '净资产(万)': round(net_sum / 10000)})
    per_month_df = pd.DataFrame(per_month_rec)
    return per_month_df


def get_predict_df(prop_df: pd.DataFrame, show_term: int, prop_amount: dict):
    today = datetime.today().date()
    all_df = []
    udf = prop_df[(prop_df['sum_amount'] != 0) | (prop_df['currency'] != 0)]

    for idx, row in udf.iterrows():
        if row['ctype'] in {1, 3}:
            start_date = datetime.strptime(row['start_date'], '%Y-%m-%d').date()
            loan = EqualDelt(row['sum_amount'], row['rate'], start_date, today, row['term_month'], row['ctype'])
        elif row['ctype'] == 0:
            loan = EqualPrincipalPayment(row['currency'], today, show_term)
        elif row['ctype'] == 2:
            start_date = datetime.strptime(row['start_date'], '%Y-%m-%d').date()
            loan = InterestLoan(row['sum_amount'], row['rate'], start_date, today, row['term_month'])
        elif row['ctype'] == 4:
            loan = FinishLoan(row['sum_amount'], row['rate'], today, row['term_month'])
        else:
            raise ValueError(f'ctype error, {row=}')
        schedule = loan.schedule()
        schedule['name'] = row['name']
        schedule['type'] = row['type']
        all_df.append(schedule)

    all_pred = pd.concat(all_df)
    all_date = sorted(list(set(all_pred['date'])))
    current_net = prop_amount['as'] * 10000 - prop_amount['de'] * 10000
    current_cash = prop_amount['cash'] * 10000
    all_c = []
    for day in all_date[:show_term]:
        recs = all_pred[all_pred['date'] == day]
        # 权益增加，现金增加
        prop_add = 0
        cash_add = 0
        detail_str = ''
        for idx, row in recs.iterrows():
            # print(row)
            if row['payment'] == 0:
                continue
            detail_str += f"{row['name']}:{round(row['payment'])},\n"
            if row['type'] <= 1:
                prop_add += row['interest']
                cash_add += row['payment']
            else:
                prop_add -= row['interest']
                cash_add -= row['payment']
        current_net += prop_add
        current_cash += cash_add
        rec = {'日期': day, '净资产变动': round(prop_add), '现金流': round(cash_add),
               '当期净资产(万)': round(current_net/10000),
               '当期现金(万)': round(current_cash/10000), '分项': detail_str}
        all_c.append(rec)

    cash_predict = pd.DataFrame(all_c[1:])
    return cash_predict
