import dash_bootstrap_components as dbc
from dash import html
from loguru import logger
from book_callback.web_fuc import get_prop_data
from OpenBookkeeping.gloab_info import prop_type_items


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
            group_item_content = dbc.Row([
                dbc.Col(row['name']),
                dbc.Col([
                    dbc.Button(html.I(className="bi bi-trash"), id={'type': 'prop_list_del', 'index': row['id']},
                               className='me-1', color='light'),
                    dbc.Button(html.I(className="bi bi-pencil-square"), id={"type": "prop_list_edit", 'index': row['id']},
                               className='me-1', color='light')
                ], style={'textAlign': 'right'})
            ])
            item = dbc.ListGroupItem(group_item_content, id={"type": "prop_list_item", "index": row['id']})
            list_items.append(item)
        accordion_item = dbc.AccordionItem(
            dbc.ListGroup(list_items, flush=True),
            title=prop_type_name,
            id=prop_type_name
        )
        div_items.append(accordion_item)
    res = dbc.Accordion(div_items, always_open=True, active_item=prop_type_items)
    return res


def get_prop_form(prop_info: tuple = None):
    """
    依据账户的信息，创建form，如果是新增，就是空form。否则是有内容的form
    :param prop_info: 数据库返回的账户信息
    :return: children
    """
    ...