import dash_bootstrap_components as dbc
from dash import html

account_list_item = dbc.Row([
    dbc.Col('账户1'),
    dbc.Col([
        dbc.Button(html.I(className="bi bi-trash"), id='ac1_edit',
            className='me-1', color='light'),
        dbc.Button(html.I(className="bi bi-pencil-square"), id='ac1_edit',
            className='me-1', color='light')],
    style={'textAlign': 'right'})
])


account_list = dbc.Stack([
    html.H4('账户列表'),
    html.Hr(),
    dbc.ListGroup(
        [
            dbc.ListGroupItem(html.H6('流动资产'), disabled=True, color='primary'),
            dbc.ListGroupItem(account_list_item),
            dbc.ListGroupItem('账户2'),
            dbc.ListGroupItem('账户3'),
            dbc.ListGroupItem(html.H6('固定资产'), disabled=True, color='primary'),
            dbc.ListGroupItem('账户1'),
            dbc.ListGroupItem('账户2'),
            dbc.ListGroupItem('账户3')
        ], flush=True)
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

