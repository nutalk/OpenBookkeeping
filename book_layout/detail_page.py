import dash_bootstrap_components as dbc
from dash import html, dcc
from book_callback.detail_fuc import get_prop_list
from config import db_path


prop_list = get_prop_list(db_path)


account_list = dbc.Stack([
    html.H4('账户列表'),
    html.Hr(),
    html.Div(prop_list, id='detail_prop_list'),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle('编辑账户')),
            dbc.ModalBody('body', id='edit_prop_body'),
            dbc.ModalFooter([
                dbc.Button('保存', id='edit_prop_save'),
                dbc.Button('取消', id='edit_prop_cancel')]
            )
        ], id='edit_prop_modal', size='lg', is_open=False
    ),
    dcc.Store(id='edit_prop_info', storage_type='session', data={}),
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


account_info = html.Div('account info')


account_detail = html.Div('account detail')

detail_layout = dbc.Row(
    [dbc.Col(account_list, md=3),
     dbc.Col([
         dbc.Row(account_info),
         dbc.Row(account_detail)
     ], md=9)]
)

