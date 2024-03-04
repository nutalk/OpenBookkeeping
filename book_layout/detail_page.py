import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
from book_callback.detail_fuc import get_prop_list
from config import db_path
from OpenBookkeeping.gloab_info import account_info_show


prop_list = get_prop_list(db_path)

account_list = dbc.Stack([
    html.H4('账户列表'),
    html.Hr(),
    html.Div(prop_list, id='detail_prop_list'),
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
        dbc.Row(account_detail),
    ], md=9)]
)
