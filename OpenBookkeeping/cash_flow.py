from datetime import date
from loan_calculator import Loan
import pandas as pd
from dateutil.relativedelta import relativedelta


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
    固定现金流
    """
    def __init__(self, currency: float, start_date, term_month: int = 12):
        self.currency = currency
        self.rdates = [start_date + relativedelta(months=i, day=1) for i in range(0, term_month + 1)]

    def schedule(self):
        days = [(d - self.rdates[0]).days for d in self.rdates]
        interest_payments = [self.currency for _ in days]
        amortizations = [0 for _ in days]
        balance = [0 for _ in days]
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




