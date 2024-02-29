import dash_bootstrap_components as dbc
from dash import html
from book_callback.detail_fuc import get_prop_list
from config import db_path


prop_list = get_prop_list(db_path)


account_list = dbc.Stack([
    html.H4('账户列表'),
    html.Hr(),
    prop_list
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

