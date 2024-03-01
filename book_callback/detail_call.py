from pathlib import Path
from dash import Output, Input, callback, html, ALL, MATCH, ctx, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from loguru import logger

from config import db_path
from OpenBookkeeping.sql_db import (query_table, add_prop, query_by_col,
                                    update_by_col, del_by_col)
from OpenBookkeeping.gloab_info import account_info_show, prop_type_items, liability_currency_types
from book_callback.detail_fuc import get_prop_list


@callback(
    [Output(f'account_info_{_}', 'children') for _ in account_info_show],
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

    return tuple(output)


#TODO 删除账户的对话框


#TODO 编辑，新增，删除账户之后，更新左侧的列表


#TODO 编辑账户信息

