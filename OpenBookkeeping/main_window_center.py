from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
from PySide6.QtCore import Qt, Signal
from loguru import logger

class MainTree(QWidget):
    ...


class LineChart(QWidget):
    ...


class PieChart(QWidget):
    ...


class MainLayouts(QWidget):
    def __init__(self):
        super().__init__()
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



