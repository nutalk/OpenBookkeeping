import json
from collections import defaultdict
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.db.models import Sum
from .models import Prop, Detail
from .forms import PropNewForm, DetailForm, PropEditForm
from .gloab_info import prop_type_ids, prop_type_items, \
    is_fake_items, liability_currency_types, account_info_show
from django.utils.translation import gettext as _
# Create your views here.


def trans_date_str(input_date: str) -> str:
    true_date = datetime.strptime(input_date, "%d/%m/%Y")
    res = true_date.strftime("%Y-%m-%d")
    return res

def retrans_date_str(input_date: str) -> str:
    true_date = datetime.strptime(input_date, "%Y-%m-%d")
    res = true_date.strftime("%d/%m/%Y")
    return res


# 账户与明细页面
def details(request):
    prop_new_form = PropNewForm(action_str='/prop_new/', form_id='prop_new', form_class='prop_new_form')
    prop_edit_form = PropEditForm(action_str='/prop_edit/', form_id='prop_edit', form_class='prop_edit_form')
    detail_new_form = DetailForm(action_str='/detail_new/', form_id='detail_new', form_class='detail_new_form')
    detail_edit_form = DetailForm(action_str='/detail_edit/', form_id='detail_edit', form_class='detail_edit_form')
    contex = {
        "type_prop": [],
        "prop_new_form": prop_new_form,
        "prop_edit_form": prop_edit_form,
        'detail_new_form': detail_new_form,
        'detail_edit_form': detail_edit_form,
        'show_info': [{'id': k, 'show': _(v)} for k, v in account_info_show.items()]
    }
    for prop_type_name, prop_type_id in prop_type_ids.items():
        rec = {'type_name': _(prop_type_name),
               'id': f"collapse_{prop_type_id}",
               'href': f"#collapse_{prop_type_id}"}
        type_prop = Prop.objects.filter(p_type=prop_type_id).values()
        rec['recs'] = [{'id': f"plg_{item['id']}", 'name': item['name']} for item in type_prop]
        contex['type_prop'].append(rec)
    template = loader.get_template('detail.html')
    return HttpResponse(template.render(contex, request))


def get_prop_from_request(request, pname = 'prop_id'):
    prop_id = request.POST.get(pname)
    *ww, id = prop_id.split('_')
    prop = Prop.objects.filter(id=id).values()[0]
    return prop


# 获取某个资产的详细信息
def prop_detail_post(request):
    if request.method == 'POST':
        prop = get_prop_from_request(request)
        result= []
        for k, v in prop.items():
            if k == 'p_type':
                res = _(prop_type_items[v])
            elif k == 'ctype':
                res = _(liability_currency_types[v])
            elif k == 'start_date':
                res = trans_date_str(v)
            elif k == 'is_fake':
                res = _(is_fake_items[v])
            else:
                res = v
            result.append({'k': k, 'v': res})
            
        result = json.dumps(result)
        return HttpResponse(result,content_type='application/json;charset=utf-8')
    else:
        return HttpResponse({}, content_type='application/json;charset=utf-8')


# 获取某个资产的明细
def prop_detail_table(request):
    if request.method == "POST":
        prop = get_prop_from_request(request)
        details = Detail.objects.filter(target_id=prop['id']).values()
        result = []
        amount = 0
        for rec in details:
            amount += rec['amount']
            rec['rem_amount'] = amount
            rec['occur_date'] = trans_date_str(rec['occur_date'])
            result.append(rec)
        result = sorted(result, key=lambda x: x['occur_date'], reverse=True)
        result = json.dumps(result)
        return HttpResponse(result,content_type='application/json;charset=utf-8')
    else:
        return HttpResponse({}, content_type='application/json;charset=utf-8')

#新增账户
def prop_new(request):
    if request.method == "POST":
        new_prop = Prop(
            name = request.POST.get('name'),
            p_type = request.POST.get('p_type'),
            start_date = retrans_date_str(request.POST.get('start_date')),
            term_month = request.POST.get('term_month'),
            rate = float(request.POST.get('rate')),
            currency=request.POST.get('currency'),
            ctype=request.POST.get('ctype'),
            comment=request.POST.get('comment'),
            is_fake = request.POST.get('is_fake')
        )
        new_prop.save()
        detail = Detail(
            target_id = new_prop,
            occur_date = retrans_date_str(request.POST.get('start_date')),
            amount = request.POST.get('init_ammount'),
            comment = _('Init ammount')
        )
        detail.save()
    return redirect("/")

# 删除账户
def prop_del(request):
    if request.method == 'POST':
        prop = get_prop_from_request(request)
        prop = Prop.objects.get(pk=prop['id'])
        prop.delete()
    return redirect("/")

# 编辑保存账户信息
def prop_edit(request):
    if request.method == "POST":
        
        prop = Prop.objects.get(pk=request.POST.get('id'))
        if prop is not None:
            prop.name = request.POST.get('name')
            prop.p_type = int(request.POST.get('p_type'))
            prop.start_date = retrans_date_str(request.POST.get('start_date'))
            prop.term_month = request.POST.get('term_month')
            prop.rate = float(request.POST.get('rate'))
            prop.currency=request.POST.get('currency')
            prop.ctype=int(request.POST.get('ctype'))
            prop.comment=request.POST.get('comment')
            prop.is_fake = int(request.POST.get('is_fake'))
            prop.save()
    return redirect("/")

# 删除明细
def detail_del(request):
    if request.method == 'POST':
        did = request.POST.get('detail_id')
        prop = Detail.objects.get(pk=did)
        prop.delete()
    return redirect("/")

# 新增明细
def detail_new(request):
    if request.method == 'POST':
        target_prop = get_prop_from_request(request, 'target_id')
        target_prop = Prop.objects.get(pk=target_prop['id'])
        detail = Detail(
            target_id = target_prop,
            occur_date = retrans_date_str(request.POST.get('occur_date')),
            amount = request.POST.get('amount'),
            comment = request.POST.get('comment')
        )
        detail.save()
    return redirect("/")

# 获取一条明细
def detail_get_post(request):
    if request.method=="POST":
        did = request.POST.get('id')
        result = Detail.objects.filter(id=did).values()[0]        
        result['occur_date'] = trans_date_str(result['occur_date'])
        res = [{'k': k, 'v': v} for k, v in result.items()]
        result = json.dumps(res)
        return HttpResponse(result,content_type='application/json;charset=utf-8')
    else:
        return HttpResponse({}, content_type='application/json;charset=utf-8')

# 编辑明细
def detail_edit(request):
    if request.method == 'POST':
        detail = Detail.objects.get(pk=request.POST.get('id'))
        if detail is not None:
            detail.occur_date = retrans_date_str(request.POST.get('occur_date'))
            detail.amount = request.POST.get('amount')
            detail.comment = request.POST.get('comment')
            detail.save()
    return redirect("/")

# 对账页面
def book_check(request):
    res = Prop.objects.annotate(remains=Sum('detail__amount')).values()
    contex = {'type_prop': []}
    output = defaultdict(list)

    for obj in res:
        if obj['remains'] is None:
            rems = 0
        else:
            rems = obj['remains']
        rec = { 'id': f"idd_{obj['id']}",'name': obj['name'], 'remains': rems}
        obj_type = prop_type_items[obj['p_type']]
        output[obj_type].append(rec)

    for k, v in output.items():
        rec = {'k': _(k), 'v': v}
        contex['type_prop'].append(rec)
    
    template = loader.get_template('check.html')
    return HttpResponse(template.render(contex, request))

# 对账数据处理
def check_submit(request):
    if request.method == 'POST':
        res = Prop.objects.annotate(remains=Sum('detail__amount')).values()
        prop_remain_dict = {int(item['id']): item['remains'] for item in res}

        for k, v in request.POST.items():
            if 'idd_' in k:
                *_i, tid = k.split('_')
                tid = int(tid)
                v = int(v)
                if prop_remain_dict[tid] != v:
                    if prop_remain_dict[tid] is None:
                        prop_remain_dict[tid] = 0
                    today = datetime.today().date()
                    today_str = today.strftime("%d/%m/%Y")
                    target_prop = Prop.objects.get(pk=tid)
                    detail = Detail(
                        target_id = target_prop,
                        occur_date = today_str,
                        amount = v - prop_remain_dict[tid],
                        comment = _("Balance Check")
                    )
                    detail.save()
    return redirect("/")
