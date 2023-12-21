"""
分析财务状况的web页面，基于plotly dash
https://fac.feffery.tech/getting-started
"""
import dash
from dash import html
import feffery_antd_components as fac
from dash.dependencies import Input, Output


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
                                menuItems=[
                                    {
                                        'component': 'Item',
                                        'props': {
                                            'key': f'k{icon}',
                                            'title': f'{title}',
                                            'icon': icon
                                        }
                                    }
                                    for icon, title in {
                                        'antd-pie-chart': "资产负债表",
                                        'antd-history': '趋势表',
                                        'antd-line-chart': '预测'
                                    }.items()
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
                                        fac.AntdTitle(
                                            '内容区示例',
                                            level=2,
                                            style={
                                                'margin': '0'
                                            }
                                        ),
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


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8156)

