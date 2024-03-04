import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
from book_callback.detail_fuc import get_prop_list
from config import db_path
from OpenBookkeeping.gloab_info import account_info_show


general_layout = html.Div(
    # 资产负债净资产
    [dbc.Row([
        dbc.Col([
            html.P('资产'),
            html.H3('5000')
        ],md=4),
        dbc.Col([
            html.P('负债'),
            html.H3('3000')
        ], md=4),
        dbc.Col([
            html.P('净资产'),
            html.H3('2000')
        ],md=4),
    ]),
    html.Hr(),
     # 资产饼图
     dbc.Row([
         # 资产
         dbc.Col([], md=6),
         # 负债
         dbc.Col([], md=6)
     ])]
)