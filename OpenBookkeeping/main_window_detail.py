from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QDoubleSpinBox, QSpinBox, QComboBox, \
    QTextEdit, QDateEdit, QListView, QSpacerItem, QSizePolicy, QDialog, QMessageBox, \
    QGroupBox, QTableView, QHeaderView
from PySide6.QtCore import QDate, Signal, QAbstractTableModel, Qt
from loguru import logger
from functools import wraps
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor

from OpenBookkeeping.new_prop import PropList
from OpenBookkeeping.sql_db import query_by_col
from OpenBookkeeping.fuc import DetailTableModel


class DetailTable(QWidget):
    def __init__(self):
        super().__init__()
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel('账户变化明细'))
        self.detail_table = QTableView(self)
        self.detail_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.detail_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.detail_model = DetailTableModel()
        self.detail_table.setModel(self.detail_model)
        right_layout.addWidget(self.detail_table)
        btn_layout = QHBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.new_btn = QPushButton('记一笔')
        self.edit_btn = QPushButton('编辑')
        self.del_but = QPushButton('删除')

        btn_layout.addItem(spacer)
        btn_layout.addWidget(self.new_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.del_but)
        right_layout.addLayout(btn_layout)

        self.setLayout(right_layout)

    def update_content(self, data: list, header: list):
        logger.debug(f'{data=}, {header=}')
        self.detail_model.update_content(data, header)
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
            headers = ['id', '账户名称', '交易日期', '交易金额', '备注', '余额']
            output = []
            sum = 0
            for row in details:
                sum += row[3]
                new_row = [row[0], prop_name] + list(row[2:]) + [sum]
                output.append(new_row)
            self.detail.update_content(output, header=headers)
        else:
            logger.error(f'length of prop invalid {info}')

