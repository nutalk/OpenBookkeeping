import dash_bootstrap_components as dbc
from dash import html, dcc
from loguru import logger
from datetime import date
from book_callback.web_fuc import get_prop_data
from OpenBookkeeping.gloab_info import prop_type_items, liability_currency_types


def get_prop_list(db_path: str):
    """
    获取账户列表，childern
    :param db_path: 数据库路径
    :return: childern
    """
    div_items = []
    prop_df = get_prop_data(db_path)
    for idx, prop_type_name in enumerate(prop_type_items):
        prop_list = prop_df[prop_df['type'] == idx]
        list_items = []
        for row_id, row in prop_list.iterrows():
            item = dbc.ListGroupItem(row['name'], id={"type": "prop_list_item", "index": row['id']})
            list_items.append(item)
        accordion_item = dbc.AccordionItem(
            dbc.ListGroup(list_items, flush=True),
            title=prop_type_name,
            id=prop_type_name
        )
        div_items.append(accordion_item)
    res = dbc.Accordion(div_items, always_open=True, start_collapsed=False)
    return res

