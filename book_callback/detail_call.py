from pathlib import Path
from dash import Output, Input, callback, html, ALL, MATCH, ctx
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from loguru import logger

from config import db_path
from OpenBookkeeping.sql_db import (query_table, add_prop, query_by_col,
                                    update_by_col, del_by_col)


@callback(
[Output("del_prop_id", "value"),
    Output('del_prop_modal', 'is_open'),
    Output('del_prop_confirm_txt', 'children')],
    Input({'type': 'prop_list_del', 'index': ALL}, "n_clicks")
)
def del_prop_confirm(prop_del_btn):
    button_clicked = ctx.triggered_id
    if button_clicked is None:
        raise PreventUpdate

    prop_id = button_clicked['index']
    info = query_by_col(db_path, 'prop', 'id', prop_id)
    details = query_by_col(db_path, 'prop_details', 'target_id', prop_id)
    if len(info) == 1:
        allert = dbc.Alert([html.P(f'账户名称: {info[0][1]}'),
                      html.P(f'账户明细: {len(details)} 条')], color='secondary')
        child_txt = [allert, html.P(f'确定删除吗？')]
        return prop_id, True, child_txt
    else:
        raise PreventUpdate





