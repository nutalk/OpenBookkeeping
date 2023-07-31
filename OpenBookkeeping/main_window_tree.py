from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTreeView, QWidget, QHBoxLayout, QApplication
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor

from OpenBookkeeping.fuc import trans_data
from loguru import logger


class MainTree(QWidget):
    def __init__(self):
        super().__init__()
        self.tree = QTreeView(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.tree)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['类别', '名称', '余额'])
        self.tree.setModel(self.model)

        self.setLayout(layout)

    def update_content(self, data: dict):
        self.model.clear()
        root = self.model.invisibleRootItem()
        for type_id, rec_dict in data.items():
            child_type = QStandardItem(str(type_id))
            color = QColor('lightGray')
            child_type.setBackground(color)
            child_name = QStandardItem('')
            child_name.setBackground(color)
            child_amount = QStandardItem(str(rec_dict['amount']))
            child_amount.setBackground(color)
            root.appendRow([child_type, child_name, child_amount])
            for rec in rec_dict['recs']:
                child_type.appendRow([
                    QStandardItem(str(v)) for v in rec
                ])
        self.tree.expandAll()



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

    def update_content(self):
        data = [(0, '2b801', 5),
                (0, '42001', 7),
                (1, 'zs', 1),
                (1, 'zh', 2)]
        data_trans = trans_data(data)
        self.left_tree.update_content(data_trans)


