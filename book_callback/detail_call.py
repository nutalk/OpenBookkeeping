from pathlib import Path
from dash import Output, Input, callback, html, ALL, MATCH, ctx, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from loguru import logger

from config import db_path
from OpenBookkeeping.sql_db import (query_table, add_prop, query_by_col,
                                    update_by_col, del_by_col)
from book_callback.detail_fuc import get_prop_list


#TODO 删除账户的对话框


#TODO 编辑，新增，删除账户之后，更新左侧的列表


#TODO 编辑账户信息

