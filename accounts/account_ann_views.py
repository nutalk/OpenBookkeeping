import json
import pandas as pd
from loguru import logger
from datetime import datetime
from django.http import JsonResponse
from .web_fuc import get_predict_res, get_amount
from .gloab_info import prop_type_ids, liability_currency_ids


def get_chart_ts(data: list) -> dict:
    """
    根据账户信息，产生prop_df，然后get_predict_res计算绘图需要的时许信息
    """
    logger.debug(data)
    today = datetime.today().date()
    today_str = today.strftime("%d/%m/%Y")
    res_conver = []
    for id, item in enumerate(data):
        rec = {'start_date': today_str, 'id': id}
        for k, v in item.items():
            if k == 'name':
                rec[k] = v
            elif k == 'type':
                rec[k] = prop_type_ids[v]
            elif k == 'ctype':
                rec[k] = liability_currency_ids[v]
            elif k == 'rate':
                rec[k] = float(v)
            else:
                rec[k] = int(v)
        res_conver.append(rec)
    prop_df = pd.DataFrame(res_conver)
    max_term = max(prop_df['term_month'])

    prop_amount = get_amount(prop_df)
    output = get_predict_res(prop_df, max_term, prop_amount)

    return output
    


def analyze_debt(request):
    """
    处理POST请求，分析每期现金流和债务余额。
    """
    if request.method == "POST":
        data = request.POST.get('ssdata')
        data = json.loads(data)

        res = get_chart_ts(data)

        return JsonResponse(res, status=200)
    else:
        return JsonResponse({"error": "只支持POST请求"}, status=405)