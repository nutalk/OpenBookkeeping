from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton,\
    QHBoxLayout, QVBoxLayout, QGridLayout, QDoubleSpinBox, QSpinBox, QComboBox, \
    QTextEdit, QDateEdit
from PySide6.QtCore import QDate
from loguru import logger

from OpenBookkeeping.sql_db import add_prop, query_table, add_liability
from OpenBookkeeping.gloab_info import prop_type_items, liability_type_items, liability_currency_types

class NewItem(QWidget):
    def __init__(self, database: str, window_title: str):
        super().__init__()
        self.database = database
        self.setWindowTitle(window_title)

        self.warring_label = QLabel('')

        self.buts_layout = QHBoxLayout()
        self.cancel_btn = QPushButton('取消')
        self.confirm_btn = QPushButton('确定')
        self.buts_layout.addWidget(self.cancel_btn)
        self.buts_layout.addWidget(self.confirm_btn)
        self.band()

    def band(self):
        self.cancel_btn.pressed.connect(self.cancel_btp_fuc)
        self.confirm_btn.pressed.connect(self.confirm_btn_fuc)

    def cancel_btp_fuc(self):
        self.close()

    def check_valid(self) -> str:
        return '还没定义好'

    def confirm_btn_fuc(self):
        check_res = self.check_valid()
        if check_res == '':
            print('confirm')
        else:
            self.warring_label.setText(check_res)
            self.warring_label.setStyleSheet("color: red;")


class NewProp(NewItem):
    def __init__(self, database: str):
        super().__init__(database, '新增资产')
        input_layout = QGridLayout()

        all_labels = dict(
            name = QLabel('名称'),
            type = QLabel('类别'),
            start_date = QLabel('开始日期'),
            currency = QLabel('月现金流'),
            comment = QLabel('备注'),
        )

        self.all_input = dict(
            name = QLineEdit(),
            type = QComboBox(),
            start_date = QDateEdit(),
            currency = QSpinBox(),
            comment = QTextEdit()
        )
        self.all_input['type'].addItems(prop_type_items)
        self.all_input['currency'].setMaximum(999999999)
        self.all_input['start_date'].setDisplayFormat("yyyy-MM-dd")
        self.all_input['start_date'].setCalendarPopup(True)
        self.all_input['start_date'].setDate(QDate.currentDate())

        for idx, _label in enumerate(all_labels.values()):
            input_layout.addWidget(_label, idx+1, 1)
        for idx, _input in enumerate(self.all_input.values()):
            input_layout.addWidget(_input, idx+1, 2)

        input_layout.addWidget(self.warring_label, idx+2, 2)
        input_layout.addLayout(self.buts_layout, idx+3, 2)
        self.setLayout(input_layout)

    def check_valid(self) -> str:
        prop_name = self.all_input['name'].text()
        prop_type = self.all_input['type'].currentIndex()
        start_date = self.all_input['start_date'].date().toString("yyyy-MM-dd")
        currency = self.all_input['currency'].value()
        comment = self.all_input['comment'].toPlainText()
        exist_names = query_table(self.database, ['name'], 'prop')
        names = [item[0] for item in exist_names]
        names = set(names)
        logger.debug(f'{prop_name=}, {prop_type=}, {currency=}, {start_date=} \
{comment=}, {self.database}')

        if not prop_name:
            return '名称不能为空'
        if prop_name in names:
            return '资产名已存在'
        
        add_prop(self.database, prop_name, prop_type,
                 currency, start_date, comment)


class NewLiability(NewItem):
    def __init__(self, database: str):
        super().__init__(database, '新增负债')
        input_layout = QGridLayout()
        all_labels = dict(
            name = QLabel('名称'),
            type = QLabel('负债类型'),
            rate = QLabel('年利率'),
            currency_type = QLabel('还款付息类型'),
            start_date = QLabel('开始日期'),
            term_month = QLabel('期数'),
            comment = QLabel('备注'))
        
        self.all_input = dict(
            name = QLineEdit(),
            type = QComboBox(),
            rate = QDoubleSpinBox(),
            currency_type = QComboBox(),
            start_date = QDateEdit(),
            term_month = QSpinBox(),
            comment = QTextEdit()
        )
        self.all_input['type'].addItems(liability_type_items)
        self.all_input['currency_type'].addItems(liability_currency_types)
        self.all_input['term_month'].setMaximum(9999)
        self.all_input['start_date'].setDisplayFormat("yyyy-MM-dd")
        self.all_input['start_date'].setCalendarPopup(True)
        self.all_input['start_date'].setDate(QDate.currentDate())

        for idx, label in enumerate(all_labels.values()):
            input_layout.addWidget(label, idx+1, 1)

        for idx, _input in enumerate(self.all_input.values()):
            input_layout.addWidget(_input, idx+1, 2)
        
        input_layout.addWidget(self.warring_label, idx+2, 2)
        input_layout.addLayout(self.buts_layout, idx+3, 2)

        self.setLayout(input_layout)

    def check_valid(self) -> str:
        _name = self.all_input['name'].text()
        _type = self.all_input['type'].currentIndex()
        _rate = self.all_input['rate'].value()
        _currency_type = self.all_input['currency_type'].currentIndex()
        _start_date = self.all_input['start_date'].date().toString("yyyy-MM-dd")
        _term_month = self.all_input['term_month'].value()
        _comment = self.all_input['comment'].toPlainText()

        exist_names = query_table(self.database, ['name'], 'liability')
        names = [item[0] for item in exist_names]
        names = set(names)
        logger.debug(f'{_name=}, {_type=}, {_currency_type=},{_rate}, {_comment=}, \
{_start_date}, {_term_month=}, {self.database}')

        if not _name:
            return '名称不能为空'
        if _name in names:
            return '资产名已存在'
        
        add_liability(self.database, _name, _type, _currency_type, _rate, _start_date,
                      _term_month, _comment)
        
        