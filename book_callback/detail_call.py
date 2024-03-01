from pathlib import Path
from dash import Output, Input, callback, html, ALL, MATCH, ctx, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from loguru import logger

from config import db_path
from OpenBookkeeping.sql_db import (query_table, add_prop, query_by_col,
                                    update_by_col, del_by_col)
from book_callback.detail_fuc import get_prop_list


# 删除账户的对话框
@callback(
[Output("del_prop_info", "data"),
    Output('del_prop_modal', 'is_open'),
    Output('del_prop_confirm_txt', 'children')],
    [Input({'type': 'prop_list_del', 'index': ALL}, "n_clicks"),
     Input('del_prop_save', 'n_clicks'),
     Input('del_prop_cancel', 'n_clicks'),],
    State('del_prop_info','data')
)
def del_prop_confirm(prop_del_btn, del_save, del_cancel, del_prop_info):
    button_clicked = ctx.triggered_id
    logger.debug(f'{button_clicked=}, {del_prop_info=}')

    if button_clicked is None:
        raise PreventUpdate

    if isinstance(button_clicked, dict):
        prop_id = button_clicked['index']
        info = query_by_col(db_path, 'prop', 'id', prop_id)
        details = query_by_col(db_path, 'prop_details', 'target_id', prop_id)
        if len(info) == 1:
            allert = dbc.Alert([html.P(f'账户名称: {info[0][1]}'),
                          html.P(f'账户明细: {len(details)} 条')], color='secondary')
            child_txt = [allert, html.P(f'确定删除吗？')]
            return {'id': prop_id, 'info': info[0]}, True, child_txt
        else:
            raise PreventUpdate
    else:
        if button_clicked == 'del_prop_cancel':
            ...
        else:
            to_del_id = del_prop_info['id']
            del_by_col(db_path, 'prop_details', 'target_id', to_del_id)
            del_by_col(db_path, 'prop', 'id', to_del_id)
        return -1, False, ''


# 编辑，新增，删除账户之后，更新左侧的列表
@callback(
    Output('detail_prop_list', 'children'),
    [Input('del_prop_save', 'n_clicks'),
     Input('edit_prop_save', "n_clicks"),]
)
def update_prop_list(del_save, edit_save):
    return get_prop_list(db_path)


# 编辑账户信息
@callback(
[Output("edit_prop_info", "data"),
    Output('edit_prop_modal', 'is_open')],
    [Input('edit_prop_save', "n_clicks"),
     Input('edit_prop_cancel', 'n_clicks'),
     Input({"type": 'prop_edit_form', "index":ALL}, 'value'),
     Input({"type": "prop_list_edit", 'index': ALL}, 'n_clicks')],
    State('edit_prop_info', 'data')
)
def edit_prop_form(edit_save, edit_cancel, form_values, prop_edit_list_btn, edit_prop_info):
    button_clicked = ctx.triggered_id
    logger.debug(f'{button_clicked=}, {edit_prop_info=}')
    logger.debug(f'{form_values=}')

    if button_clicked is None:
        raise PreventUpdate

    if not isinstance(button_clicked, dict):
        raise PreventUpdate

    return -1, True

