from pathlib import Path
from dash import Output, Input, callback, html, ALL, MATCH, ctx, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from loguru import logger

from config import db_path
from OpenBookkeeping.sql_db import (query_table, add_prop, query_by_col,
                                    update_by_col, del_by_col)
from book_callback.detail_fuc import get_prop_list


@callback(
[Output("edit_prop_info", "data"),
    Output('del_prop_modal', 'is_open'),
    Output('del_prop_confirm_txt', 'children')],
    [Input({'type': 'prop_list_del', 'index': ALL}, "n_clicks"),
     Input('del_prop_save', 'n_clicks'),
     Input('del_prop_cancel', 'n_clicks'),],
    State('edit_prop_info','data')
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


@callback(
    Output('detail_prop_list', 'children'),
    Input('edit_prop_info', 'data')
)
def update_prop_list(prop_info):
    return get_prop_list(db_path)



