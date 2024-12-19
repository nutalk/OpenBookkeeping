import json
import pandas as pd
from loguru import logger
from datetime import datetime
from django.http import JsonResponse
from .web_fuc import EqualDelt, InterestLoan, FinishLoan, \
    EqualPrincipalPayment, get_predict_res


def calculate_cash_flow(item: dict) -> pd.DataFrame:
    """
    依据账户类别，计算现金流
    """
    logger.debug(item)
    # item = json.loads(item)
    name = item.get("name", "")
    loan_type = item.get("categorySmall", "")
    principal = float(item.get("currentValue", 0))
    annual_rate = float(item.get("annualRate", 0))
    periods = int(item.get("periods", 0))
    cash_flow = int(item.get("cashFlow", 0))
    stype = 1 # 1: 资产， 2： 负债
    if loan_type in ['等额本息', '先息后本', '等额本金', '到期还本付息']:
        stype = 2
    today = datetime.today().date()
    if loan_type =='月度':
        loan = EqualPrincipalPayment(principal, cash_flow, today, periods)
    elif loan_type == '等额本息':
        loan = EqualDelt(principal, annual_rate, today, today, periods, 1)
    elif loan_type == '等额本金':
        loan = EqualDelt(principal, annual_rate, today, today, periods, 3)
    elif loan_type in ['先息后本', '按月收利']:
        loan = InterestLoan(principal, annual_rate, today, today, periods)
    elif loan_type in ['到期还本付息', '到期收本息']:
        loan = FinishLoan(principal, annual_rate, today, today, periods)
    else:
        raise ValueError(f'error: {loan_type=}')
    schedule = loan.schedule()
    schedule['name'] = name
    schedule['type'] = stype
    return schedule
    


def analyze_debt(request):
    """
    处理POST请求，分析每期现金流和债务余额。
    """
    if request.method == "POST":
        data = request.POST.get('ssdata')
        data = json.loads(data)
        results = []

        for item in data:
            # 计算现金流和余额
            schedule = calculate_cash_flow(item)
            results.append(schedule)

        all_schedule = pd.concat(results)
        predict_res = get_predict_res(all_schedule)

        return JsonResponse(predict_res, status=200)
    else:
        return JsonResponse({"error": "只支持POST请求"}, status=405)