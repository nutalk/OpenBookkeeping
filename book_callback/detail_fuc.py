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


def create_input_line(label: str, input_type: str, index: int):
    """
    创建输入行
    :param label: 标签
    :param input_type: 输入类型
    :param index: 索引
    :return:
    """

    line = dbc.Row(
        [
            dbc.Label(label, width=2),
            dbc.Col(dbc.Input(id={"type": 'prop_edit_form', "index": index}, type=input_type),
                    width=10)
        ], className='mb-3'
    )
    return line


def get_prop_form(prop_info: tuple = None):
    """
    依据账户的信息，创建form，如果是新增，就是空form。否则是有内容的form
    :param prop_info: 数据库返回的账户信息
    :return: children
    """
    name_input = create_input_line('账户名称', 'text', 0)
    type_input = dbc.Row(
        [
            dbc.Label('账户类型', width=2),
            dbc.Col(
                dbc.Select(id={"type": 'prop_edit_form', "index": 1},
                           options=[{"label": item, 'value': idx} for idx, item in enumerate(prop_type_items)]),
                width=10
            )
        ], className='mb-3'
    )
    start_date_input = dbc.Row(
        [
            dbc.Label('开始日期', width=2),
            dbc.Col(dcc.DatePickerSingle(id={"type": 'prop_edit_form', "index": 2},
                                         display_format='Y-M-D',
                                         date=date.today()),
                    width=10)
        ], className='mb-3'
    )
    term_num_input = create_input_line('期限', 'number', 3)
    interest_rate_input = create_input_line('年化利率', 'number', 4)
    current_input = create_input_line('现金流', 'number', 5)
    pay_type_input = dbc.Row(
        [
            dbc.Label('还款方式', width=2),
            dbc.Col(
                dbc.Select(id={"type": 'prop_edit_form', "index": 6},
                           options=[{"label": item, 'value': idx} for idx, item in enumerate(liability_currency_types)]),
                width=10
            )
        ], className='mb-3'
    )
    note_input = create_input_line('备注', 'text', 7)

    total_form = dbc.Form([name_input, type_input, start_date_input, term_num_input,
                           interest_rate_input, current_input, pay_type_input, note_input])
    return total_form

