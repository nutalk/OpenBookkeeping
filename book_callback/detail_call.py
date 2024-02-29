from pathlib import Path
from dash import Output, Input, callback, html, ALL, MATCH, ctx
from dash.exceptions import PreventUpdate
from loguru import logger

from OpenBookkeeping.sql_db import (query_table, add_prop, query_by_col,
                                    update_by_col, del_by_col)


@callback(
[Output("del_prop_id", "value"),
    Output('del_prop_modal', 'is_open'),
    Output('del_prop_confirm_txt', 'children')],
    Input({'type': 'prop_list_del', 'index': ALL}, "n_clicks")
)
def del_prop_confirm(values):
    button_clicked = ctx.triggered_id
    if button_clicked is None:
        raise PreventUpdate
    prop_id = button_clicked['index']
    return prop_id, True, f'你确定删除账户{prop_id}吗？'