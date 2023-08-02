from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout, QFormLayout, QDoubleSpinBox, QSpinBox, QComboBox, \
    QTextEdit, QDateEdit, QListView, QSpacerItem, QSizePolicy, QDialog, QMessageBox, \
    QGroupBox, QTableView, QHeaderView
from PySide6.QtCore import QDate, Signal, QAbstractTableModel, Qt, QModelIndex
from loguru import logger
from functools import wraps
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor

from OpenBookkeeping.new_prop import PropList
from OpenBookkeeping.sql_db import query_by_col
from OpenBookkeeping.fuc import DetailTableModel


class DetailForm(QWidget):
    def __init__(self, target_names: list, current_id: int = 0):
        super().__init__()
        layout = QFormLayout()
        self.target_name = QComboBox()
        self.target_name.addItems(target_names)
        self.target_name.setCurrentIndex(current_id)
        self.occur_date = QDateEdit()
        self.occur_date.setDisplayFormat("yyyy-MM-dd")
        self.occur_date.setCalendarPopup(True)
        self.occur_date.setDate(QDate.currentDate())

        self.amount = QSpinBox()
        self.amount.setMaximum(999999)

        self.note = QTextEdit()

        layout.addRow('账户名称', self.target_name)
        layout.addRow('发生日期', self.occur_date)
        layout.addRow('金额', self.amount)
        layout.addRow('备注', self.note)

        btn_layout = QHBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.new_btn = QPushButton('确定')
        self.edit_btn = QPushButton('取消')

        btn_layout.addItem(spacer)
        btn_layout.addWidget(self.new_btn)
        btn_layout.addWidget(self.edit_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)


class DetailTable(QWidget):
    def __init__(self):
        super().__init__()
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel('账户变化明细'))
        self.detail_table = QTableView(self)
        self.detail_table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.detail_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.detail_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.detail_model = DetailTableModel()
        self.detail_table.setModel(self.detail_model)
        right_layout.addWidget(self.detail_table)
        btn_layout = QHBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.new_btn = QPushButton('记一笔')
        self.edit_btn = QPushButton('编辑')
        self.edit_btn.pressed.connect(self.edit_line)
        self.del_but = QPushButton('删除')
        self.del_but.pressed.connect(self.del_line)

        btn_layout.addWidget(self.new_btn)
        btn_layout.addItem(spacer)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.del_but)
        right_layout.addLayout(btn_layout)

        self.setLayout(right_layout)

    def update_content(self, data: list, header: list):
        logger.debug(f'{data=}, {header=}')
        self.detail_model.update_content(data, header)
        # 通知viewer
        self.detail_model.layoutChanged.emit()
        index = QModelIndex()
        self.detail_table.setCurrentIndex(index)

    def _edit_del_line(self) -> QModelIndex:
        row_index = self.detail_table.currentIndex()
        logger.debug(row_index.row())
        if row_index.row() == -1:
            self.mesg = QMessageBox()
            self.mesg.warning(self, '请先选中', '请先选中明细条目')
        return row_index

    def edit_line(self):
        index = self._edit_del_line()

    def del_line(self):
        index = self._edit_del_line()

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

