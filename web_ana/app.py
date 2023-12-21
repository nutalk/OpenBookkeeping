"""
分析财务状况的web页面，基于plotly dash
https://fac.feffery.tech/getting-started
"""
import dash
from dash import html
import feffery_antd_components as fac
from dash.dependencies import Input, Output


main_menu_dict = {
    'antd-pie-chart': "资产负债表",
    'antd-history': '趋势表',
    'antd-line-chart': '预测'
}


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        fac.AntdLayout(
            [
                fac.AntdHeader(
                    fac.AntdTitle(
                        'OpenBookkeeping',
                        level=2,
                        style={
                            'color': 'white',
                            'margin': '0'
                        }
                    ),
                    style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'alignItems': 'center'
                    }
                ),
                fac.AntdLayout(
                    [
                        fac.AntdSider(
                            [
                            fac.AntdMenu(
                                id='main_menu',
                                menuItems=[
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'{icon}',
                                            'title': f'{title}',
                                            'icon': icon
                                        }
                                    }
                                    for icon, title in main_menu_dict.items()
                                ],
                            mode='inline',
                            style={
                                'height': '100%',
                                'overflow': 'hidden auto'
                                }
                            )
                            ],
                            style={
                                'backgroundColor': 'rgb(240, 242, 245)',
                                'display': 'flex',
                                'justifyContent': 'center'
                            }
                        ),
                        fac.AntdLayout(
                            [
                                fac.AntdContent(
                                    html.Div(
                                        'OpenBookkeeping',
                                        id='main_disp',
                                        style={
                                            'display': 'flex',
                                            'height': '100%',
                                            'justifyContent': 'center',
                                            'alignItems': 'center'
                                        }
                                    ),
                                    style={
                                        'backgroundColor': 'white'
                                    }
                                )
                            ]
                        )
                    ],
                    style={
                        'height': '100%'
                    }
                )
            ]
        )
    ],
    style={
        'height': '100vh',
        'border': '1px solid rgb(241, 241, 241)',
        'display': 'flex',
    }
)


# 定义回调函数串起相关交互逻辑
@app.callback(
    Output('main_disp', 'children'),
    Input('main_menu', 'currentKey')
)
def handle_main_menu(current_key):
    print(current_key)
    return f'{current_key}'


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8156)

