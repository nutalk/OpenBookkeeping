from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QDoubleSpinBox, QSpinBox, QComboBox, \
    QTextEdit, QDateEdit, QListView, QSpacerItem, QSizePolicy
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
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel('账户列表'))

        self.list = QListView(self)
        self.list_model = QStandardItemModel()
        self.list.setModel(self.list_model)
        left_layout.addWidget(self.list)

        button_layout = QHBoxLayout()
        self.new_btn = QPushButton('新增')
        self.del_btn = QPushButton('删除')
        button_layout.addWidget(self.new_btn)
        button_layout.addWidget(self.del_btn)
        left_layout.addLayout(button_layout)

        main_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()
        right_btn_layout = QHBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        right_btn_layout.addItem(spacer)
        self.conf_btn = QPushButton('确认')
        self.cancel_btn = QPushButton('取消')
        right_btn_layout.addWidget(self.conf_btn)
        right_btn_layout.addWidget(self.cancel_btn)

        right_layout.addWidget(QLabel('账户详情'))
        input_form_layout = self.get_input_form()
        right_layout.addLayout(input_form_layout)
        right_layout.addLayout(right_btn_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)
        self.update_content()
        self.resize(500, 400)

    def get_input_form(self):
        input_form_layout = QGridLayout()
        all_labels = dict(
            name=QLabel('名称'),
            type=QLabel('类型'),
            start_date=QLabel('开始日期'),
            term_month=QLabel('期数'),
            rate=QLabel('年利率'),
            currenty=QLabel('月现金流'),
            currency_type=QLabel('还款方式'),
            comment=QLabel('备注'))

        self.all_input = dict(
            name=QLineEdit(),
            type=QComboBox(),
            start_date=QDateEdit(),
            term_month=QSpinBox(),
            rate=QDoubleSpinBox(),
            currency=QSpinBox(),
            currency_type=QComboBox(),
            comment=QTextEdit()
        )
        self.all_input['type'].addItems(prop_type_items)
        self.all_input['currency_type'].addItems(liability_currency_types)
        self.all_input['currency'].setMaximum(9999999)
        self.all_input['term_month'].setMaximum(9999)
        self.all_input['start_date'].setDisplayFormat("yyyy-MM-dd")
        self.all_input['start_date'].setCalendarPopup(True)
        self.all_input['start_date'].setDate(QDate.currentDate())

        for idx, label in enumerate(all_labels.values()):
            input_form_layout.addWidget(label, idx + 1, 1)

        for idx, _input in enumerate(self.all_input.values()):
            input_form_layout.addWidget(_input, idx + 1, 2)
        return input_form_layout

    def update_content(self):
        props = [
            '2b801',
            '42001'
        ]
        for prop in props:
            item = QStandardItem(prop)
            self.list_model.appendRow(item)






