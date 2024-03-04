from pathlib import Path
from dash import Output, Input, callback, html, ALL, MATCH, ctx, State
from dash.exceptions import PreventUpdate
from dash.dash_table import DataTable
from dash.dash_table.Format import Format
from loguru import logger
import pandas as pd

from config import db_path
from OpenBookkeeping.sql_db import (query_table, add_prop, query_by_col,
                                    update_by_col, del_by_col)
from OpenBookkeeping.gloab_info import account_info_show, prop_type_items, liability_currency_types
from book_callback.detail_fuc import get_prop_list, get_prop_form


# 更新账户基本信息
@callback(
    [Output(f'account_info_{_}', 'children') for _ in account_info_show] +
    [Output('current_prop_info', 'data')],
    [Input({"type": "prop_list_item", "index": ALL}, 'n_clicks')]
)
def update_account_page(n_clicks):
    btn_id = ctx.triggered_id
    if btn_id is None:
        raise PreventUpdate
    prop_res = query_by_col(db_path, 'prop', 'id', btn_id['index'])
    logger.debug(f'{prop_res=}')
    if len(prop_res) != 1:
        raise PreventUpdate
    rec = prop_res[0]
    output = []
    for idx, rec_content in enumerate(rec[1:]):
        if idx == 1:
            content = prop_type_items[rec_content]
        elif idx == 6:
            content = liability_currency_types[rec_content]
        elif idx == 4:
            content = f'{rec_content}%'
        else:
            content = rec_content
        output.append(content)
    output.append({'id': btn_id['index'], 'name': rec[1]})

    return tuple(output)


# 更新账户明细表格
@callback(
    Output(f'account_detail_table', 'children'),
    [Input({"type": "prop_list_item", "index": ALL}, 'n_clicks')]
)
def update_account_detail_table(n_clicks):
    btn_id = ctx.triggered_id
    if btn_id is None:
        raise PreventUpdate
    details = query_by_col(db_path, 'prop_details', 'target_id', btn_id['index'])
    details = sorted(details, key=lambda x: x[2])
    columns = [
        dict(id='id', name='ID', type='numeric'),
        dict(id='date', name='日期', type='datetime'),
        dict(id='amount', name='交易金额', type='numeric', format=Format(group=True)),
        dict(id='balance', name='余额', type='numeric', format=Format(group=True)),
        dict(id='remark', name='备注', type='text'),
    ]
    data = []
    sum = 0
    for row in details:
        sum += row[3]
        data.append(dict(
            id=row[0],
            date=row[2],
            amount=row[3],
            balance=sum,
            remark=row[4],
        ))
    data = sorted(data, key=lambda x: x['date'], reverse=True)
    table = DataTable(columns=columns, data=data, page_size=10)
    return table


#删除账户的对话框
@callback(
    [Output('del_prop_modal', 'is_open'),
     Output('del_prop_confirm_txt', 'children'),
     Output('to_update_prop_table', 'data', allow_duplicate=True)],
    [Input('prop_del_btn','n_clicks'),
     Input('del_prop_save', 'n_clicks'),
     Input('del_prop_cancel', 'n_clicks'),
     Input('current_prop_info', 'data')],
    prevent_initial_call=True
)
def show_del_prop_modal(del_btn, del_save, del_cancel, prop_info):
    btn_id = ctx.triggered_id
    to_update = {'to_update': False}
    if btn_id == 'prop_del_btn':
        return True, f"确定删除 {prop_info['name']} 吗？", to_update
    elif btn_id == 'del_prop_save':
        del_by_col(db_path, 'prop', 'id', prop_info['id'])
        return False, '', {'to_update': True}
    elif btn_id == 'del_prop_cancel':
        return False, '', to_update
    else:
        raise PreventUpdate


#编辑，新增，删除账户之后，更新左侧的列表
@callback(
    Output('detail_prop_list', 'children'),
    Input('to_update_prop_table', 'data')
)
def update_prop_list(to_update):
    if to_update['to_update']:
        return get_prop_list(db_path)
    else:
        raise PreventUpdate

#TODO 编辑账户信息
@callback(
    [Output('edit_prop_modal', 'is_open'),
     Output('edit_prop_body', 'children'),
     Output('to_update_prop_table', 'data', allow_duplicate=True)],
    [Input('prop_edit_btn','n_clicks'),
     Input('edit_prop_save', 'n_clicks'),
     Input('edit_prop_cancel', 'n_clicks'),
    Input('current_prop_info', 'data')],
    prevent_initial_call=True
)
def show_edit_prop_modal(edit_btn, edit_save, edit_cancel, prop_info):
    btn_id = ctx.triggered_id
    to_update = {'to_update': False}
    if btn_id == 'prop_edit_btn':
        form_output = get_prop_form()
        return True, form_output, to_update
    elif btn_id == 'edit_prop_save':
        del_by_col(db_path, 'prop', 'id', prop_info['id'])
        return False, '', {'to_update': True}
    elif btn_id == 'edit_prop_cancel':
        return False, '', to_update
    else:
        raise PreventUpdate
