from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QDoubleSpinBox, QSpinBox, QComboBox, \
    QTextEdit, QDateEdit, QListView, QSpacerItem, QSizePolicy, QDialog, QMessageBox, \
    QGroupBox, QTableView
from PySide6.QtCore import QDate, Signal, QAbstractTableModel, Qt
from loguru import logger
from functools import wraps
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor

from OpenBookkeeping.new_prop import PropList
from OpenBookkeeping.sql_db import query_by_col


class DetailTableModel(QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self._data = []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        if len(self._data) == 0:
            return 0
        else:
            return len(self._data[0])

    def update_content(self, data: list):
        self._data = data


class DetailTable(QWidget):
    def __init__(self):
        super().__init__()
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel('账户变化明细'))
        self.detail_table = QTableView(self)
        self.detail_model = DetailTableModel()
        self.detail_table.setModel(self.detail_model)
        right_layout.addWidget(self.detail_table)
        self.setLayout(right_layout)

    def update_content(self, data: list):
        logger.debug(f'{data=}')
        self.detail_model.update_content(data)
        # 通知viewer
        self.detail_model.layoutChanged.emit()


class DetailPage(QWidget):
    def __init__(self):
        super().__init__()
        self.database = None
        self.current_name = None
        layout = QHBoxLayout()
        self.prop_list = PropList(self.database)
        self.prop_list.select_sig.connect(self.update_prop_detail)
        self.prop_list.setMaximumWidth(200)
        layout.addWidget(self.prop_list)

        self.detail = DetailTable()
        layout.addWidget(self.detail)

        self.setLayout(layout)

    def update_content(self, database: str):
        self.database = database
        self.prop_list.database = database
        self.prop_list.update_content()

    def update_prop_detail(self, prop_name):
        self.current_name = prop_name
        info = query_by_col(self.database, 'prop', 'name', prop_name)
        if len(info) == 1:
            prop_id = info[0][0]
            details = query_by_col(self.database, 'prop_details', 'target_id', prop_id)
            self.detail.update_content(details)
        else:
            logger.error(f'length of prop invalid {info}')

