from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QDoubleSpinBox, QSpinBox, QComboBox, \
    QTextEdit, QDateEdit, QListView, QSpacerItem, QSizePolicy, QDialog, QMessageBox, \
    QGroupBox
from PySide6.QtCore import QDate, Signal
from loguru import logger
from functools import wraps
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor

from OpenBookkeeping.gloab_info import prop_type_items, liability_currency_types
from OpenBookkeeping.sql_db import (query_table, add_prop, query_by_col,
                                    update_by_col, del_by_col)


class PropName(QDialog):
    conf_sig = Signal(str)

    def __init__(self, exist_props: list):
        super(PropName, self).__init__()
        self.setWindowTitle('账户名称')
        layout = QVBoxLayout()
        self.editer = QLineEdit()
        layout.addWidget(self.editer)

        self.exist_props = exist_props
        self.warring_label = QLabel('')
        layout.addWidget(self.warring_label)

        right_btn_layout = QHBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        right_btn_layout.addItem(spacer)
        self.conf_btn = QPushButton('确认')
        self.cancel_btn = QPushButton('取消')
        right_btn_layout.addWidget(self.conf_btn)
        right_btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(right_btn_layout)
        self.setLayout(layout)

        self.conf_btn.clicked.connect(self.conf_emit)
        self.cancel_btn.clicked.connect(self.cancel)

    def conf_emit(self):
        new_name = self.editer.text()
        logger.debug(f'{new_name=}')
        if new_name in self.exist_props:
            self.warring_label.setText(f'{new_name}已存在')
        elif new_name == '':
            self.warring_label.setText(f'名称不能为空，不能重复')
        else:
            self.conf_sig.emit(new_name)
            self.close()

    def cancel(self):
        self.editer.setText('')
        self.close()


class DeleteConfirm(QDialog):
    conf_sig = Signal(str)

    def __init__(self, prop_name: str):
        super().__init__()
        self.setWindowTitle('删除确认')
        layout = QVBoxLayout()
        self.prop_name = prop_name

        self.warring_label = QLabel(f'确认删除账户：{prop_name}？')
        layout.addWidget(self.warring_label)

        right_btn_layout = QHBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        right_btn_layout.addItem(spacer)
        self.conf_btn = QPushButton('确认')
        self.cancel_btn = QPushButton('取消')
        right_btn_layout.addWidget(self.conf_btn)
        right_btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(right_btn_layout)
        self.setLayout(layout)

        self.conf_btn.clicked.connect(self.conf_emit)
        self.cancel_btn.clicked.connect(self.cancel)

    def conf_emit(self):
        self.conf_sig.emit(self.prop_name)
        self.close()

    def cancel(self):
        self.close()


class PropInfo(QWidget):
    def __init__(self, database: str):
        super().__init__()
        self.database = database
        layout = QVBoxLayout()
        right_btn_layout = QHBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        right_btn_layout.addItem(spacer)
        self.conf_btn = QPushButton('保存')
        right_btn_layout.addWidget(self.conf_btn)
        self.conf_btn.clicked.connect(self.commit_info)

        layout.addWidget(QLabel('账户详情'))
        input_form_layout = self.get_input_form()
        layout.addLayout(input_form_layout)
        layout.addLayout(right_btn_layout)
        self.setLayout(layout)

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

        for item in self.all_input.values():
            item.setDisabled(True)

        for idx, label in enumerate(all_labels.values()):
            input_form_layout.addWidget(label, idx + 1, 1)

        for idx, _input in enumerate(self.all_input.values()):
            input_form_layout.addWidget(_input, idx + 1, 2)
        return input_form_layout

    def update_content(self, info: tuple):
        self.all_input['name'].setText(info[1])
        self.all_input['type'].setCurrentIndex(info[2])
        self.all_input['type'].setEnabled(True)
        self.all_input['start_date'].setDate(QDate.fromString(info[3], 'yyyy-MM-dd'))
        self.all_input['start_date'].setEnabled(True)
        self.all_input['term_month'].setValue(info[4])
        self.all_input['term_month'].setEnabled(True)
        self.all_input['rate'].setValue(info[5])
        self.all_input['rate'].setEnabled(True)
        self.all_input['currency'].setValue(info[6])
        self.all_input['currency'].setEnabled(True)
        self.all_input['currency_type'].setCurrentIndex(info[7])
        self.all_input['currency_type'].setEnabled(True)
        self.all_input['comment'].setText(info[8])
        self.all_input['comment'].setEnabled(True)

    def commit_info(self):
        val = dict(
            type=self.all_input['type'].currentIndex(),
            start_date=self.all_input['start_date'].date().toString("yyyy-MM-dd"),
            term_month=self.all_input['term_month'].value(),
            rate=self.all_input['rate'].value(),
            currency=self.all_input['currency'].value(),
            ctype=self.all_input['currency_type'].currentIndex(),
            comment=self.all_input['comment'].toPlainText()
        )
        update_by_col(self.database, 'prop', 'name', self.all_input['name'].text(), val)


class PropList(QWidget):
    select_sig = Signal(str, int)

    def __init__(self, database:str):
        super().__init__()
        self.exist_props = []
        self.database = database
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel('账户列表'))

        self.list = QListView(self)
        self.list_model = QStandardItemModel()
        self.list.setModel(self.list_model)
        self.list.selectionModel().currentChanged.connect(self.update_prop_info)
        left_layout.addWidget(self.list)
        self.setLayout(left_layout)

    def update_prop_info(self, current, pre):
        prop_name = current.data()
        self.select_sig.emit(prop_name, current.row())

    def update_content(self):
        self.list_model.clear()
        if self.database is None:
            props = []
        else:
            props = query_table(self.database, ['name'], 'prop')
        self.exist_props = [item[0] for item in props]
        for prop in self.exist_props:
            item = QStandardItem(prop)
            self.list_model.appendRow(item)


class NewProp(QWidget):
    def __init__(self, database: str):
        super().__init__()
        self.exist_props = []
        self.left_groupbox = QGroupBox(self)
        self.right_groupbox = QGroupBox(self)
        self.setWindowTitle('管理账户')
        self.database = database
        self.current_name = None
        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        self.left_groupbox.setLayout(left_layout)
        self.left_groupbox.setMaximumWidth(200)

        self.prop_list = PropList(self.database)
        self.prop_list.select_sig.connect(self.update_prop_info)
        left_layout.addWidget(self.prop_list)

        button_layout = QHBoxLayout()
        self.new_btn = QPushButton('新增')
        self.new_btn.clicked.connect(self.new_prop_form)
        self.del_btn = QPushButton('删除')
        self.del_btn.clicked.connect(self.del_prop)
        button_layout.addWidget(self.new_btn)
        button_layout.addWidget(self.del_btn)
        left_layout.addLayout(button_layout)

        main_layout.addWidget(self.left_groupbox)
        right_layout = QHBoxLayout()
        self.prop_edit_widget = PropInfo(self.database)
        right_layout.addWidget(self.prop_edit_widget)
        self.right_groupbox.setLayout(right_layout)
        main_layout.addWidget(self.right_groupbox)

        self.setLayout(main_layout)
        self.update_content()
        self.resize(500, 400)

    def update_content(self):
        self.prop_list.update_content()

    def update_prop_info(self, prop_name):
        self.current_name = prop_name
        info = query_by_col(self.database, 'prop', 'name', prop_name)
        if len(info) == 1:
            self.prop_edit_widget.update_content(info[0])
        else:
            logger.error(f'length of prop invalid {info}')

    def update_after(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            self.update_content()
            return res
        return wrapper

    def new_prop_form(self):
        self.dlog = PropName(self.exist_props)
        self.dlog.conf_sig.connect(self.new_prop_to_sql)
        self.dlog.show()

    @update_after
    def new_prop_to_sql(self, prop_name: str):
        add_prop(self.database, prop_name)

    @update_after
    def del_prop(self):
        if self.current_name is None:
            logger.error(f'not selected')
        else:
            self.alt = DeleteConfirm(self.current_name)
            self.alt.show()
            self.alt.conf_sig.connect(self.del_prop_sql)

    @update_after
    def del_prop_sql(self, prop_name):
        logger.debug(f'del {prop_name}')
        info = query_by_col(self.database, 'prop', 'name', prop_name)
        if len(info) == 1:
            rec = info[0]
            prop_id = rec[0]
            del_by_col(self.database, 'prop_details', 'target_id', prop_id)
            del_by_col(self.database, 'prop', 'name', prop_name)
        else:
            logger.error(f'length of prop invalid {info}')











