import pandas as pd
import numpy as np
from datetime import datetime

from datetime import date
from loan_calculator import Loan
import pandas as pd
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from .models import Prop, Detail


class EqualDelt:
    def __init__(self, amount: float, rate: float, start_date, today, term_month: int, ctype: int):
        """
        等额本息，等额本金
        """
        end_date = start_date + relativedelta(months=term_month)
        self.terms_left = (end_date.year - today.year) * 12 + end_date.month - today.month

        schedult_type = {1: 'progressive-price-schedule',
                         3: "constant-amortization-schedule"}
        rdates = [today + relativedelta(months=i, day=1) for i in range(0, self.terms_left + 1)]
        self.loan = Loan(amount, rate/100, rdates[0], rdates[1:],
                         amortization_schedule_type=schedult_type[ctype])

    def schedule(self):
        reference_date = self.loan.start_date
        dates = [reference_date] + self.loan.return_dates

        lines = list(
            zip(
                dates,
                map(lambda d: (d - reference_date).days,
                    dates),
                self.loan.balance,
                [0] + self.loan.amortizations,
                [0] + self.loan.interest_payments,
                [0] + self.loan.due_payments,
            )
        )
        return pd.DataFrame(lines, columns=['date', 'days', 'balance', 'amortization', 'interest', 'payment'])


class InterestLoan:
    def __init__(self, amount: float, rate: float, start_date, today, term_month: int):
        """
        先息后本
        """
        end_date = start_date + relativedelta(months=term_month)
        self.terms_left = (end_date.year - today.year) * 12 + end_date.month - today.month
        self.amount = amount
        self.rate = rate / 100
        self.rdates = [today + relativedelta(months=i, day=1) for i in range(0, self.terms_left + 1)]

    def schedule(self):
        days = [(d - self.rdates[0]).days for d in self.rdates]
        rdays = []
        for idx in range(len(days)):
            if idx == 0:
                rdays.append(0)
            else:
                rdays.append(days[idx] - days[idx - 1])
        interest_payments = [self.amount * self.rate / 365 * d for d in rdays]
        amortizations = [0 for _ in days[: -1]]
        amortizations.append(self.amount)
        balance = [self.amount for _ in days[: -1]]
        balance.append(0)
        due_payments = [i + a for i, a in zip(interest_payments, amortizations)]

        lines = list(
            zip(
                self.rdates,
                days,
                balance,
                amortizations,
                interest_payments,
                due_payments,
            )
        )
        return pd.DataFrame(lines, columns=['date', 'days', 'balance', 'amortization', 'interest', 'payment'])


class FinishLoan(InterestLoan):
    """
    到期还本付息
    """

    def schedule(self):
        days = [(d - self.rdates[0]).days for d in self.rdates]
        interest_payments = [0 for d in days[:-1]]
        final_interest = self.amount * self.rate * self.term_month / 12
        interest_payments.append(final_interest)

        amortizations = [0 for _ in days[: -1]]
        amortizations.append(self.amount)
        balance = [self.amount for _ in days[: -1]]
        balance.append(0)
        due_payments = [i + a for i, a in zip(interest_payments, amortizations)]

        lines = list(
            zip(
                self.rdates,
                days,
                balance,
                amortizations,
                interest_payments,
                due_payments,
            )
        )
        return pd.DataFrame(lines, columns=['date', 'days', 'balance', 'amortization', 'interest', 'payment'])


class EqualPrincipalPayment:
    """
    固定现金流,现金流不影响账户金额
    """
    def __init__(self, amount: int, currency: float, start_date, term_month: int = 12):
        self.currency = currency
        self.amount = amount
        self.rdates = [start_date + relativedelta(months=i, day=1) for i in range(0, term_month + 1)]

    def schedule(self):
        days = [(d - self.rdates[0]).days for d in self.rdates]
        interest_payments = [self.currency for _ in days]
        amortizations = [0 for _ in days]
        balance = [self.amount for _ in days]
        due_payments = [i + a for i, a in zip(interest_payments, amortizations)]

        lines = list(
            zip(
                self.rdates,
                days,
                balance,
                amortizations,
                interest_payments,
                due_payments,
            )
        )
        return pd.DataFrame(lines, columns=['date', 'days', 'balance', 'amortization', 'interest', 'payment'])


# 获取特定id的账户
def get_prop_df(allow_idx: set = None) -> pd.DataFrame:
    """
    return:
```
    name  sum_amount  type  id  p_type  start_date  term_month  rate  currency  ctype comment  remains
0   房子     3000000     0   1       0  01/06/2023           0   0.0      5000      0          3000000
1   房贷     1800000     2   2       2  01/06/2023         360   3.8         0      1          1800000
```
    """
    total_res = Prop.objects.annotate(remains=Sum('detail__amount')).values()
    all_prop = []
    for prop in total_res:
        if allow_idx is not None and int(prop['id']) not in allow_idx:
            continue
        rec = {'name': prop['name'],
                'sum_amount': prop['remains'],
                'type': prop['p_type']}
        rec.update(prop)
        all_prop.append(rec)
    prop_df = pd.DataFrame(all_prop)
    prop_df.fillna(0, inplace=True)
    return prop_df


def get_amount(prop_df: pd.DataFrame) -> dict:
    as_amount = np.sum(prop_df[prop_df['type'] <= 1]['sum_amount'])
    de_amount = np.sum(prop_df[prop_df['type'] >= 2]['sum_amount'])
    ne_amount = as_amount - de_amount
    cash = np.sum(prop_df[prop_df['type'] == 1]['sum_amount'])
    return {'as': as_amount, 'de': de_amount,
            'ne': ne_amount, 'cash': cash}


def get_schedule(prop_df, adjust_today: bool = False, show_term: int = None)->pd.DataFrame:
    
    all_df = []
    udf = prop_df[(prop_df['sum_amount'] != 0) | (prop_df['currency'] != 0)]

    if show_term is None:
        show_term = max(udf['term_month'])
        if show_term == 0:
            show_term = 24

    for idx, row in udf.iterrows():
        if adjust_today:
            today = datetime.today().date()
        else:
            today = datetime.strptime(row['start_date'], "%d/%m/%Y").date()

        if row['ctype'] in {1, 3}:
            start_date = datetime.strptime(row['start_date'], "%d/%m/%Y").date()
            loan = EqualDelt(row['sum_amount'], row['rate'], start_date, today, row['term_month'], row['ctype'])
        elif row['ctype'] == 0:
            loan = EqualPrincipalPayment(row['sum_amount'],row['currency'], today, show_term)
        elif row['ctype'] == 2:
            start_date = datetime.strptime(row['start_date'], "%d/%m/%Y").date()
            loan = InterestLoan(row['sum_amount'], row['rate'], start_date, today, row['term_month'])
        elif row['ctype'] == 4:
            loan = FinishLoan(row['sum_amount'], row['rate'], today, row['term_month'])
        else:
            raise ValueError(f'ctype error, {row=}')
        schedule = loan.schedule()
        schedule['name'] = row['name']
        schedule['type'] = row['type']
        schedule['account_id'] = row['id']
        all_df.append(schedule)

    all_pred = pd.concat(all_df)
    return all_pred


def get_predict_res(prop_df: pd.DataFrame, show_term: int, prop_amount: dict):
    """
    预测各月的现金流情况
    :param prop_df:
    :param show_term:
    :param prop_amount:
    :return:
    """
    
    current_net = prop_amount['as'] - prop_amount['de']
    current_cash = prop_amount['cash']
    current_det = prop_amount['de']
    result = {
        'total_series':[
            {'name':'净资产',
             'data': []},
             {'name': '负债',
              'data': []},
              {'name': "现金",
               'data': []}
        ],
        'cash_series':[
            {'name': '净资产变动',
             'data': []},
             {'name': '现金变动',
              'data': []}
        ]
    }
    all_pred = get_schedule(prop_df, adjust_today=True, show_term=show_term)
    all_date = sorted(list(set(all_pred['date'])))
    for id, day in enumerate(all_date[1:]):
        if id >= show_term:
            break
        recs = all_pred[all_pred['date'] == day]
        # 权益增加，现金增加
        prop_add = 0
        cash_add = 0
        det_add = 0
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
                det_add -= row['amortization']
        current_net += prop_add
        current_cash += cash_add
        current_det += det_add
        x = day.strftime("%m-%d-%Y")
        result['total_series'][0]['data'].append({'x': x, 'y':round(current_net/10000)})
        result['total_series'][1]['data'].append({'x': x, "y":round(current_det/10000)})
        result['total_series'][2]['data'].append({'x':x, "y":round(current_cash/10000)})
        result['cash_series'][0]['data'].append({'x':x, "y":round(prop_add)})
        result['cash_series'][1]['data'].append({'x':x, "y":round(cash_add)})

    return result


def get_next_cash(prop_df: pd.DataFrame, show_term: int):
    """
    下个月的现金流组成
    """
    result = {
        'income':[
            {'name':'本金',
             'data': []},
             {'name': '利息',
              'data': []},
        ],
        'income_categories':[],

        'outcome':[
            {'name': '本金',
             'data': []},
             {'name': '利息',
              'data': []}
        ],
        'outcome_categories': [],
        'income_total':0,
        'outcome_total': 0,
        'netcome_total': 0
    }
    all_pred = get_schedule(prop_df, adjust_today=True, show_term=show_term)
    all_id = sorted(list(set(all_pred['account_id'])))
    for id, account_id in enumerate(all_id):
        recs = all_pred[all_pred['account_id'] == account_id]
        for idx, row in recs.iterrows():
            # print(row)
            if row['payment'] == 0:
                continue
            if row['type'] <= 1:
                # 资产
                prop_add = round(row['interest'])
                det_add = round(row['amortization'])
                result['income'][0]['data'].append(det_add)
                result['income'][1]['data'].append(prop_add)
                result['income_categories'].append(row['name'])
                result['income_total'] += round(row['payment'])
            else:
                # 负债
                prop_add = round(row['interest'])
                det_add = round(row['amortization'])
                result['outcome'][0]['data'].append(det_add)
                result['outcome'][1]['data'].append(prop_add)
                result['outcome_categories'].append(row['name'])
                result['outcome_total'] += round(row['payment'])
            break
    result['netcome_total'] = f"￥{result['income_total'] - result['outcome_total']:,}"
    result['income_total'] = f"￥{result['income_total']:,}"
    result['outcome_total'] = f"￥{result['outcome_total']:,}"

    return result