from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTreeView, QWidget, QHBoxLayout, QApplication
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor
from loguru import logger
from datetime import datetime
from dateutil.relativedelta import relativedelta

from OpenBookkeeping.sql_db import query_table, query_by_str
from OpenBookkeeping.gloab_info import prop_type_items


class MainTree(QWidget):
    def __init__(self):
        super().__init__()
        self.tree = QTreeView(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.tree)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['类别', '名称', '余额', '利率', '到期日', '现金流'])
        self.tree.setModel(self.model)

        self.setLayout(layout)

    def update_content(self, data: dict):
        self.model.clear()
        root = self.model.invisibleRootItem()  # 根节点
        for type_id, rec_dict in data.items():
            child_type = QStandardItem(rec_dict['type_name'])  # 账户类别节点
            color = QColor('lightGray')
            child_type.setBackground(color)
            # [name, amount, f"{round(rate, 2)}%", end_date, 0]
            child_name = QStandardItem('')
            child_name.setBackground(color)
            child_amount = QStandardItem(str(rec_dict['amount']))
            child_amount.setBackground(color)
            child_rate = QStandardItem('')
            child_rate.setBackground(color)
            child_end_date = QStandardItem('')
            child_end_date.setBackground(color)
            child_currency = QStandardItem(str(rec_dict['currency']))
            child_currency.setBackground(color)
            root.appendRow([child_type, child_name, child_amount, child_rate, child_end_date, child_currency])  # 账户类别节点加入tree
            for rec in rec_dict['recs']:
                child_type.appendRow([
                    QStandardItem(str(v)) for v in rec  # 账户加入类别节点之下
                ])
        self.tree.expandAll()

    def trans_data(self, data: list) -> dict:
        """
        tuple数据转换成tree能用的dict数据
        :param data:
        :return:
        """
        data_rec = {}
        for rec in data:
            type_id, name, start_date, term_month, rate, currency, ctype, amount = rec
            if amount is None:
                amount = 0

            start_date_time = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_time = start_date_time + relativedelta(months=term_month)
            end_date = end_date_time.date().strftime('%Y-%m-%d')
            # ['类别', '名称', '余额', '利率', '到期日', '现金流']
            total_currency = 0  # TODO 现金流应该是按利率计算的
            show_rec = [prop_type_items[type_id], name, amount, f"{round(rate, 2)}%", end_date, total_currency]
            if data_rec.get(type_id) is None:
                data_rec[type_id] = {'type_name': prop_type_items[type_id],
                                     'amount': amount, 'currency': total_currency, 'recs': [show_rec]}
            else:
                data_rec[type_id]['amount'] += amount
                data_rec[type_id]['currency'] += total_currency
                data_rec[type_id]['recs'].append(show_rec)
        return data_rec



class LineChart(QWidget):
    ...


class PieChart(QWidget):
    ...


class PageOneWidget(QWidget):
    def __init__(self, database: str = None):
        super().__init__()
        self.database = database
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.left_tree = MainTree()
        left_layout.addWidget(self.left_tree)

        self.info_chart = PieChart()
        self.his_chart = LineChart()
        right_layout.addWidget(self.info_chart)
        right_layout.addWidget(self.his_chart)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def update_content(self, database: str):
        self.database = database
        query_str = """
        select type, name, start_date, term_month, rate, currency, ctype, sum(amount) from prop 
        LEFT outer join prop_details
        on prop.id = prop_details.target_id group by name;
        """
        all_props = query_by_str(self.database, query_str)
        for rec in all_props:
            logger.debug(f'{rec}')
        data_trans = self.left_tree.trans_data(all_props)
        self.left_tree.update_content(data_trans)


