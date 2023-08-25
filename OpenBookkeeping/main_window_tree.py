from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTableView
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice, QLegend
from PySide6.QtWidgets import QTreeView, QWidget, QHBoxLayout, QApplication
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor, QPen
from PySide6.QtCore import Qt
from loguru import logger
from datetime import datetime
from dateutil.relativedelta import relativedelta

from OpenBookkeeping.sql_db import query_table, query_by_str
from OpenBookkeeping.gloab_info import prop_type_items
import pyqtgraph as pg


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
        self.model.setHorizontalHeaderLabels(['类别', '名称', '余额', '利率', '到期日', '现金流'])
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
            if amount == 0:
                continue
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
    def __init__(self):
        super().__init__()
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('w')
        layout = QVBoxLayout()
        layout.addWidget(self.graph_widget)
        self.setLayout(layout)
        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        # plot data: x, y values
        pen = pg.mkPen(color=(25, 25, 25), width=3)
        self.graph_widget.plot(hour, temperature, pen=pen)


class PieChart(QWidget):
    def __init__(self, chart_name: str):
        super().__init__()
        self.series = QPieSeries()
        self.series.hovered.connect(self.on_hover)
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setTheme(QChart.ChartTheme.ChartThemeBlueNcs)
        self.chart.setTitle(chart_name)
        self.chart_view = QChartView(self.chart)
        self.chart_view.setMinimumHeight(300)
        self.chart_view.setMaximumWidth(300)

    def set_data(self, input_data: list):
        self.series.clear()
        for (rec_name, rec_value) in input_data:
            self.series.append(rec_name, rec_value)
        self.series.setLabelsVisible(True)
        self.series.setLabelsPosition(QPieSlice.LabelInsideHorizontal)
        lables = [i.label() for i in self.series.slices()]
        for slice in self.series.slices():
            slice.setLabel(f"{round(slice.percentage() * 100)}%")

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignRight)
        for i, label in enumerate(lables):
            self.chart.legend().markers(self.series)[i].setLabel(label)

    def on_hover(self, slice):
        for exi_slice in self.series.slices():
            exi_slice.setExploded(False)
        slice.setExploded(True)


class PagePie(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.prop_pie = PieChart('资产')
        self.liability_pie = PieChart('负债')
        layout.addWidget(self.prop_pie.chart_view)
        layout.addWidget(self.liability_pie.chart_view)
        # layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)


class PageOneWidget(QWidget):
    def __init__(self, database: str = None):
        super().__init__()
        self.database = database
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.left_tree = MainTree()
        left_layout.addWidget(self.left_tree)

        self.pie_chart = PagePie()
        self.his_chart = LineChart()
        self.pie_chart.setMaximumWidth(600)
        self.his_chart.setMaximumWidth(600)
        right_layout.addWidget(self.pie_chart)
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
        prop_data = []
        liability_data = []
        for rec in all_props:
            type_id, name, start_date, term_month, rate, currency, ctype, amount = rec
            if amount is None or amount == 0:
                continue
            if type_id in {0, 1}:
                prop_data.append((name, amount))
            else:
                liability_data.append((name, amount))

        self.pie_chart.prop_pie.set_data(prop_data)
        self.pie_chart.liability_pie.set_data(liability_data)


