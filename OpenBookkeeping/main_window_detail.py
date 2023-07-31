from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QDoubleSpinBox, QSpinBox, QComboBox, \
    QTextEdit, QDateEdit, QListView, QSpacerItem, QSizePolicy, QDialog, QMessageBox, \
    QGroupBox, QTableView
from PySide6.QtCore import QDate, Signal, QAbstractTableModel, Qt
from loguru import logger
from functools import wraps
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor

from OpenBookkeeping.new_prop import PropList


class DetailTableModel(QAbstractTableModel):

    def __init__(self, data: list):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class DetailPage(QWidget):
    def __init__(self):
        super().__init__()
        self.database = None
        layout = QHBoxLayout(self)
        self.setLayout(layout)
        self.prop_list = PropList(self.database)
        layout.addWidget(self.prop_list)

        right_layout = QVBoxLayout(self)
        self.detail_table = QTableView(self)
        data = [(1, 'haha'), (2, 'baba')]
        self.detail_model = DetailTableModel(data)
        self.detail_table.setModel(self.detail_model)
        right_layout.addWidget(self.detail_table)
        layout.addLayout(right_layout)

    def update_content(self, database: str):
        self.database = database
        self.prop_list.database = database
        self.prop_list.update_content()

