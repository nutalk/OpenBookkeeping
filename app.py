import streamlit as st
from pathlib import Path
import numpy as np
from web_ana.web_fuc import get_prop_data, get_amount, get_month_history_data, get_predict_df
from OpenBookkeeping.gloab_info import prop_type_items

db_path = st.text_input('数据库路径')
history_month_term = st.slider("历史月份数", 6, 24, 12)
predict_month_term = st.slider("预测月份数", 6, 24, 12)
st.divider()

if db_path == '' or not Path(db_path).exists():
    st.error(f'请输入正确的db_path: {db_path}')
else:
    prop_data = get_prop_data(db_path)
    amount_info = get_amount(prop_data)

    col1, col2 = st.columns(2)

    with col1:
        st.caption(f":chart: 总资产")
        st.subheader(f"{amount_info['as']}万")
        st.caption("	:moneybag: 净资产")
        st.subheader(f"{amount_info['ne']}万", divider="gray")
        for i in range(2):
            fix_as = prop_data[(prop_data['type'] == i) & (prop_data['sum_amount'] != 0)]
            st.caption(f"{prop_type_items[i]}: {round(np.sum(fix_as['sum_amount']) / 10000)}万")
            st.dataframe(fix_as[['name', 'type_cn', 'sum_amount']])

    with col2:
        st.caption(f":currency_exchange: 负债")
        st.subheader(f"{amount_info['de']}万")
        st.caption(":yen: 现金")
        st.subheader(f"{amount_info['cash']}万", divider="gray")
        for i in range(2, 4):
            fix_as = prop_data[(prop_data['type'] == i) & (prop_data['sum_amount'] != 0)]
            st.caption(f"{prop_type_items[i]}: {round(np.sum(fix_as['sum_amount']) / 10000)}万")
            st.dataframe(fix_as[['name', 'type_cn', 'sum_amount']])

    st.subheader("历史趋势")
    history_df = get_month_history_data(db_path, history_month_term)
    st.line_chart(history_df, x='日期', y=['负债(万)', '净资产(万)'])
    st.dataframe(history_df)

    st.subheader("现金流预测")
    predict_df = get_predict_df(prop_data, predict_month_term, amount_info)
    st.line_chart(predict_df, x='日期', y=['现金流', '净资产变动'])
    st.dataframe(predict_df)