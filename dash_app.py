from dash import Dash, dcc, html, callback, Input, Output
import dash
import dash_bootstrap_components as dbc

from book_layout.detail_page import detail_layout
import book_callback.detail_call


app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=False,
    prevent_initial_callbacks="initial_duplicate"
)

server = app.server

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("账户概况", href="/", active="exact"),
                dbc.NavLink("记账", href="/detail", active="exact"),
                dbc.NavLink("报表", href="/ana", active="exact")
            ],
            brand="OpenBookKeeping",
            color="primary",
            dark=True,
        ),
        dbc.Container(id="page-content", className="pt-4"),
    ]
)


@callback(Output("page-content", "children"),
          [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return 'home'
    elif pathname == "/detail":
        return detail_layout
    elif pathname == '/ana':
        return 'ana'
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True)
