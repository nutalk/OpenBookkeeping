import json
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.http import HttpResponse
from django.template import loader
from django.db.models import Sum
from django.utils.translation import gettext as _
from .models import Prop, Detail
from .web_fuc import get_amount, get_predict_res, get_prop_df, get_schedule, get_next_cash
from .gloab_info import history_month_term, prop_type_ids


# 报表页面
def report(request):
    contex = {}
    template = loader.get_template('report.html')
    return HttpResponse(template.render(contex, request))


# 资产组成的饼图、资产、负载和净值数值
def post_total_info(request):
    if request.method == 'POST':
        total_info = {'assets': 0,
                      'debt': 0,
                      'cash': 0}
        total_res = Prop.objects.annotate(remains=Sum('detail__amount')).values()
        assets_names, assets_remains,  dets_names, dets_remains = [], [], [], []
        for res in total_res:
            if res['remains'] == 0 or res['remains'] is None:
                continue
            ptype = int(res['p_type'])
            if ptype == 0:
                total_info['assets'] += res['remains']
                assets_names.append(res['name'])
                assets_remains.append(res['remains'])
            elif ptype == 1:
                total_info['assets'] += res['remains']
                total_info['cash'] += res['remains']
                assets_names.append(res['name'])
                assets_remains.append(res['remains'])
            else:
                total_info['debt'] += res['remains']
                dets_names.append(res['name'])
                dets_remains.append(res['remains'])

        total_info['net'] = total_info['assets'] - total_info['debt']

        total_info = [{'k': k, 'v': f"￥{v:,}"} for k, v in total_info.items()]
        result = {'total': total_info, 'an': assets_names, 'ar': assets_remains,
                  'dn': dets_names, 'dr': dets_remains}
        result = json.dumps(result)
        return HttpResponse(result,content_type='application/json;charset=utf-8')
    else:
        return HttpResponse({}, content_type='application/json;charset=utf-8')


# 各月资产负债的变化
def post_month_history(request):
    result = {}
    if request.method == 'POST':
        recs = []
        all_details = Detail.objects.all()
        for detail in all_details:
            rec = {'type': detail.target_id.p_type,
                   'name': detail.target_id.name,
                   'target_id': detail.target_id.pk,
                   'o_date': datetime.strptime(detail.occur_date, "%d/%m/%Y").date(),
                   'amount': detail.amount}
            recs.append(rec)

        prop_detail_df = pd.DataFrame(recs)

        td = relativedelta(months=1, day=1)
        next_month_first_day = datetime.today().date() + td

        result['series'] = [
            {'name': '资产',
             'data': []},
             {'name': '负债',
              'data': []},
              {'name': '净值',
               'data': []}
        ]
        result['table'] = []
        result['detail'] = []
        for i in range(0-history_month_term, 1, 1):
            end_date = next_month_first_day + relativedelta(months=i, day=1)
            end_df = prop_detail_df[prop_detail_df['o_date'] < end_date]
            detail_df = end_df[['type','target_id', 'name','amount']]
            end_detail = detail_df.groupby(['type', 'target_id']).sum()
            
            if end_detail.empty:
                end_detailres = []
            else:
                end_detailres = []
                for idx, row in end_detail.iterrows():
                    type_rec = '资产' if idx[0] <= 1 else '负债'
                    name_rec = Prop.objects.filter(pk=idx[1]).values()[0]['name']
                    amount = row['amount']
                    end_detailres.append({'type': type_rec, 'name': name_rec, 'amount': amount})
            prop_sum = np.sum(end_df[end_df['type'] <= 1]['amount'])
            det_sum = np.sum(end_df[end_df['type'] > 1]['amount'])
            net_sum = prop_sum - det_sum
            x = end_date.strftime("%m-%d-%Y")
            result['series'][0]['data'].append({'x':x,"y": round(prop_sum / 10000, 2)})
            result['series'][1]['data'].append({'x':x,"y": round(det_sum / 10000, 2)})
            result['series'][2]['data'].append({'x':x,"y": round(net_sum/ 10000, 2)})
            result['table'].append({
                'occur_date': end_date.strftime("%Y-%m-%d"),
                'prop': f"{prop_sum:,}",
                'det': f"{det_sum:,}",
                'net': f"{net_sum:,}"
            })
            result['detail'].append(end_detailres)

    result = json.dumps(result)
    return HttpResponse(result, content_type='application/json;charset=utf-8')

# 下个月的现金流、权益变化
def cash_change_next_month(request):
    result = {}
    if request.method == 'POST':
        prop_df = get_prop_df()
        result = get_next_cash(prop_df, 4)
    result = json.dumps(result)
    return HttpResponse(result, content_type='application/json;charset=utf-8')

# 预测现金流和净值变动
def post_month_predict(request):
    result = {}
    if request.method == 'POST':
        prop_df = get_prop_df()
        prop_amount = get_amount(prop_df)
        result = get_predict_res(prop_df, show_term=36, prop_amount=prop_amount)
    result = json.dumps(result)
    return HttpResponse(result, content_type='application/json;charset=utf-8')


# 账户分析页面
def account_ana(request):
    contex = {'type_prop': []}
    for prop_type_name, prop_type_id in prop_type_ids.items():
        rec = {'type_name': prop_type_name,
               'id': f"collapse_{prop_type_id}",
               'href': f"#collapse_{prop_type_id}"}
        type_prop = Prop.objects.filter(p_type=prop_type_id).values()
        rec['recs'] = [{'id': f"plg_{item['id']}", 'name': item['name']} for item in type_prop]
        contex['type_prop'].append(rec)
    template = loader.get_template('account_ana.html')
    return HttpResponse(template.render(contex, request))


# 获取特定账户的资产负债变化
def post_account_ana(request):
    result = {}
    if request.method == 'POST':
        all_id = request.POST.get('all_id')
        ids = []
        for id_str in all_id[1:].split("|"):
            _, idx = id_str.split("_")
            ids.append(int(idx))
        if ids:
            ids = set(ids)
            prop_df = get_prop_df(ids)
            # prop_amount = get_amount(prop_df)
            schedule = get_schedule(prop_df)
            all_date = sorted(list(set(schedule['date'])))
            result['long_series'] = [
                {
                    "name": "负债",
                    "data": []
                },
                {
                    "name": "资产",
                    "data": [],
                },
                {
                    "name": "净值",
                    "data": []
                }]
            result['short_series'] = [
                {
                    "name": "现金变动",
                    "data": []
                }
            ]
            for day in all_date[1:]:
                # 资产总额，债务，现金增加，净值变动
                prop, det, cash_add = 0, 0, 0
                recs = schedule[schedule['date'] == day]
                for idx, row in recs.iterrows():
                    if row['type'] <= 1:
                        prop += row['balance']
                        cash_add += row['payment']
                    else:
                        cash_add -= row['payment']
                        det += row['balance']
                x = day.strftime("%m-%d-%Y")
                result['long_series'][0]['data'].append({'x':x,"y": det/10000})
                result['long_series'][1]['data'].append({"x":x, "y": prop/10000})
                result['long_series'][2]['data'].append({'x':x, 'y': (prop-det)/10000})
                result['short_series'][0]['data'].append({'x': x, 'y': cash_add/10000})

    result = json.dumps(result)
    return HttpResponse(result, content_type='application/json;charset=utf-8')