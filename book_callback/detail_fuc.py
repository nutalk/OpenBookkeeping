import dash_bootstrap_components as dbc
from dash import html
from book_callback.web_fuc import get_prop_data
from OpenBookkeeping.gloab_info import prop_type_items


def get_prop_list(db_path: str):
    """
    获取账户列表，childern
    :param db_path: 数据库路径
    :return: childern
    """
    list_items = []
    prop_df = get_prop_data(db_path)
    for idx, prop_type_name in enumerate(prop_type_items):
        prop_list = prop_df[prop_df['type'] == idx]
        item = dbc.ListGroupItem(html.H6(prop_type_name), disabled=True, color='primary')
        list_items.append(item)
        for row_id, row in prop_list.iterrows():
            group_item_content = dbc.Row([
                dbc.Col(row['name']),
                dbc.Col([
                    dbc.Button(html.I(className="bi bi-trash"), id=f"prop_list_{row['id']}_del",
                               className='me-1', color='light'),
                    dbc.Button(html.I(className="bi bi-pencil-square"), id=f"prop_list_{row['id']}_edit",
                               className='me-1', color='light')
                ], style={'textAlign': 'right'})
            ])
            item = dbc.ListGroupItem(group_item_content, id=f"prop_list_{row['id']}")
            list_items.append(item)
    return dbc.ListGroup(list_items, flush=True, id='prop_list')
