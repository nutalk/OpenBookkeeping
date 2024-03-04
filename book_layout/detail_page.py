import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
from book_callback.detail_fuc import get_prop_list, get_prop_form
from config import db_path
from OpenBookkeeping.gloab_info import account_info_show


prop_list = get_prop_list(db_path)

account_list = dbc.Stack([
    html.H4('账户列表'),
    html.Hr(),
    html.Div(prop_list, id='detail_prop_list'),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle('编辑账户')),
            dbc.ModalBody(get_prop_form(), id='edit_prop_body'),
            dbc.ModalFooter([
                dbc.Button('保存', id='edit_prop_save'),
                dbc.Button('取消', id='edit_prop_cancel')]
            )
        ], id='edit_prop_modal', size='lg', is_open=False
    ),
    dcc.Store(id='current_prop_info', storage_type='session', data={}),
    dcc.Store(id='to_update_prop_table', storage_type='session', data={}),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle('删除账户')),
            dbc.ModalBody([
                html.Div('确定删除该账户吗？', id='del_prop_confirm_txt'),
            ]),
            dbc.ModalFooter([
                dbc.Button('确定', id='del_prop_save'),
                dbc.Button('取消', id='del_prop_cancel')]
            )
        ], id='del_prop_modal', is_open=False
    )
]
)


def get_row(id_str, show_label: str):
    row = dbc.Row([
        dbc.Col(show_label, md=2),
        dbc.Col('----', id=f'account_info_{id_str}', md=10),
    ])
    return row


account_info = html.Div([
    html.H4('---', id='account_info_name'),
    html.Hr(),
    *[get_row(k, v) for k, v in account_info_show.items() if k != 'name']
])

df = pd.DataFrame(
    {
        "First Name": ["Arthur", "Ford", "Zaphod", "Trillian"],
        "Last Name": ["Dent", "Prefect", "Beeblebrox", "Astra"],
    }
)

table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

account_detail = html.Div(table, id='account_detail_table')

detail_layout = dbc.Row([
    dbc.Col(account_list, md=3),
    dbc.Col([
        dbc.Row(account_info),
        html.Hr(),
        dbc.ButtonGroup(
            [dbc.Button("编辑账户", id='prop_edit_btn', outline=True, color="primary"),
             dbc.Button("删除账户", id='prop_del_btn', outline=True, color="primary"),
             dbc.Button("记一笔", id='prop_add_detail_btn', outline=True, color="primary"),
             dbc.Button('核对余额', id='prop_check_amount_btn', outline=True, color="primary")]),
        html.Hr(),
        dbc.Row(account_detail),
        html.Hr(),
        dbc.ButtonGroup([
            dbc.Button('编辑记录', id='detail_edit_btn', outline=True, color="primary"),
            dbc.Button('删除记录', id='detail_del_btn', outline=True, color="primary")
        ])

    ], md=9)]
)
