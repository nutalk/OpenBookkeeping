from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QDoubleSpinBox, QSpinBox, QComboBox, \
    QTextEdit, QDateEdit, QListView
from PySide6.QtCore import QDate
from loguru import logger
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor

from OpenBookkeeping.gloab_info import prop_type_items, liability_currency_types
from OpenBookkeeping.sql_db import add_prop, query_table, add_liability, query_by_col, update_by_col


class NewProp(QWidget):
    def __init__(self, database: str):
        super().__init__()
        self.database = database
        main_layout = QHBoxLayout()
        left_list_layout = QVBoxLayout()
        left_list_layout.addWidget(QLabel('账户列表'))

        self.list = QListView(self)
        self.list_model = QStandardItemModel()
        self.list.setModel(self.list_model)
        left_list_layout.addWidget(self.list)

        button_layout = QHBoxLayout()
        self.new_btn = QPushButton('新增')
        self.del_btn = QPushButton('删除')
        button_layout.addWidget(self.new_btn)
        button_layout.addWidget(self.del_btn)
        left_list_layout.addLayout(button_layout)

        main_layout.addLayout(left_list_layout)

        right_layout = QVBoxLayout()
        right_form_layout = QGridLayout()
        right_btn_layout = QVBoxLayout()

        self.conf_btn = QPushButton('确认')
        self.cancel_btn = QPushButton('取消')
        right_btn_layout.addWidget(self.conf_btn)
        right_btn_layout.addWidget(self.cancel_btn)

        right_layout.addWidget(QLabel('账户详情'))
        right_layout.addLayout(right_form_layout)
        right_layout.addLayout(right_btn_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)
        self.update_content()

    def update_content(self):
        props = [
            '2b801',
            '42001'
        ]
        for prop in props:
            item = QStandardItem(prop)
            self.list_model.appendRow(item)






