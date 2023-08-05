"""
账户明细页面
"""

from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout, QFormLayout, QDoubleSpinBox, QSpinBox, QComboBox, \
    QTextEdit, QDateEdit, QListView, QSpacerItem, QSizePolicy, QDialog, QMessageBox, \
    QGroupBox, QTableView, QHeaderView
from PySide6.QtCore import QDate, Signal, QAbstractTableModel, Qt, QModelIndex
from loguru import logger
from functools import wraps
from PySide6.QtGui import QStandardItemModel, QStandardItem, QColor

from OpenBookkeeping.new_prop import PropList
from OpenBookkeeping.sql_db import query_by_col, update_by_col, add_detail
from OpenBookkeeping.fuc import DetailTableModel


class DetailForm(QWidget):
    def __init__(self, database: str, detail_id: int, target_names: list, current_id: int = 0,
                 amount: int = 0, note: str = ''):
        """
        明细修改或者新增的表单的父类
        :param database: 数据库路径
        :param detail_id: 明细的数据库id
        :param target_names: 账户名称的列表
        :param current_id: 当前账户在账户名称列表中的id
        :param amount: 金额
        :param note: 备注
        """
        super().__init__()
        self.database = database
        self.detail_id = detail_id
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.target_name = QComboBox()
        self.target_name.addItems(target_names)
        self.target_name.setCurrentIndex(current_id)
        self.occur_date = QDateEdit()
        self.occur_date.setDisplayFormat("yyyy-MM-dd")
        self.occur_date.setCalendarPopup(True)
        self.occur_date.setDate(QDate.currentDate())

        self.amount = QSpinBox()
        self.amount.setMaximum(999999)
        self.amount.setValue(amount)
        self.note = QTextEdit()
        self.note.setText(note)

        form_layout.addRow('账户名称', self.target_name)
        form_layout.addRow('发生日期', self.occur_date)
        form_layout.addRow('金额', self.amount)
        form_layout.addRow('备注', self.note)

        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        spacer = QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.cfm_btn = QPushButton('确定')
        self.cfm_btn.pressed.connect(self.cfm_fuc)
        self.cal_btn = QPushButton('取消')
        self.cal_btn.pressed.connect(self.cal_fuc)

        btn_layout.addItem(spacer)
        btn_layout.addWidget(self.cfm_btn)
        btn_layout.addWidget(self.cal_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def cfm_fuc(self):
        """
        确定按钮对应的功能，需要继承后子类内进行实现
        :return:
        """
        logger.debug(f'confrm')
        ...

    def cal_fuc(self):
        self.close()


class DetailEditForm(DetailForm):
    close_sig = Signal()

    def __init__(self, database: str, detail_id: int, target_names: list, current_id: int = 0,
                 amount: int = 0, note: str = ''):
        """
        明细表单修改
        :param database: 数据库路径
        :param detail_id: 明细的数据库id
        :param target_names: 账户名称的列表
        :param current_id: 当前账户在账户名称列表中的id
        :param amount: 金额
        :param note: 备注
        """
        super().__init__(database, detail_id, target_names, current_id, amount, note)
        self.target_name.setEnabled(False)

    def cfm_fuc(self):
        values = {'occur_date': self.occur_date.date().toString("yyyy-MM-dd"),
                  'amount': self.amount.value(),
                  'notes': self.note.toPlainText()}
        update_by_col(self.database, 'prop_details', 'id', self.detail_id, values)
        self.close_sig.emit()
        self.close()


class DetailNewForm(DetailForm):
    close_sig = Signal()

    def __init__(self, database: str, detail_id: int, target_names: list, current_id: int = 0,
                 amount: int = 0, note: str = ''):
        """
        明细表单--新增明细
        :param database: 数据库路径
        :param detail_id: 明细的数据库id
        :param target_names: 账户名称的列表
        :param current_id: 当前账户在账户名称列表中的id
        :param amount: 金额
        :param note: 备注
        """
        super().__init__(database, detail_id, target_names, current_id, amount, note)
        self.target_name.setEnabled(False)

    def cfm_fuc(self):
        values = {'occur_date': self.occur_date.date().toString("yyyy-MM-dd"),
                  'amount': self.amount.value(),
                  'notes': self.note.toPlainText()}
        target_name = self.target_name.currentText()
        exist_target_id = query_by_col(self.database, 'prop', 'name', target_name)
        assert len(exist_target_id) == 1, f'{exist_target_id=}, not valid'
        target_id = exist_target_id[0][0]
        add_detail(self.database, target_id, **values)
        self.close_sig.emit()
        self.close()


class DetailTable(QWidget):
    edit_sig = Signal()

    def __init__(self, prop_names: list):
        super().__init__()
        self.prop_names = prop_names
        self.current_prop_idx = None
        self.database = None
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

    def update_content(self, data: list, header: list, prop_idx: int, database: str):
        self.database = database
        logger.debug(f'{data=}, {header=}, {prop_idx}')
        self.current_prop_idx = prop_idx
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
        """
        编辑明细
        :return:
        """
        index = self._edit_del_line()
        if index.row() >= 0:
            line = self.detail_model.get_row(index.row())
            self.edit_form = DetailEditForm(self.database, line[0], self.prop_names,
                                            self.current_prop_idx, amount=line[3],
                                            note=line[4])
            self.edit_form.close_sig.connect(self.finish_edit)
            self.edit_form.show()

    def finish_edit(self):
        self.edit_sig.emit()

    def del_line(self):
        """
        删除明细
        :return:
        """
        index = self._edit_del_line()
        # TODO


class DetailPage(QWidget):
    def __init__(self):
        super().__init__()
        self.database = None
        self.current_name = None
        self.prop_idx = None
        layout = QHBoxLayout()
        self.prop_list = PropList(self.database)
        self.prop_list.select_sig.connect(self.update_prop_detail)
        self.prop_list.setMaximumWidth(200)
        layout.addWidget(self.prop_list)

        self.detail = DetailTable([])
        self.detail.new_btn.pressed.connect(self.new_detail)
        self.detail.edit_sig.connect(self.update_after_edit_detail)
        layout.addWidget(self.detail)

        self.setLayout(layout)

    def update_after_edit_detail(self):
        logger.debug(f'update detail here')
        self.update_prop_detail(self.current_name, self.prop_idx)

    def update_content(self, database: str):
        self.database = database
        self.prop_list.database = database
        self.prop_list.update_content()
        self.detail.prop_names = self.prop_list.exist_props

    def update_prop_detail(self, prop_name: str, prop_idx: int):
        """
        当选中账户后，更新当前选中的账户名称和所处的行号
        :param prop_name: 账户名称
        :param prop_idx: 在list中的行号
        :return:
        """
        self.current_name = prop_name
        self.prop_idx = prop_idx
        info = query_by_col(self.database, 'prop', 'name', prop_name)
        if len(info) == 1:
            prop_id = info[0][0]
            details = query_by_col(self.database, 'prop_details', 'target_id', prop_id)
            details = sorted(details, key=lambda x: x[2])
            headers = ['id', '账户名称', '交易日期', '交易金额', '备注', '余额']
            output = []
            sum = 0
            for row in details:
                sum += row[3]
                new_row = [row[0], prop_name] + list(row[2:]) + [sum]
                output.append(new_row)
            self.detail.update_content(output, header=headers, prop_idx=prop_idx, database=self.database)
        else:
            logger.error(f'length of prop invalid {info}')

    def new_detail(self):
        """
        新增明细条目
        :return:
        """
        current_prop_idx = self.prop_list.list.currentIndex().row()
        logger.debug(f'new prop, {current_prop_idx=}')
        self.new_detail_form = DetailNewForm(self.database, 0, self.prop_list.exist_props,
                                             current_prop_idx)
        self.new_detail_form.close_sig.connect(self.update_after_edit_detail)
        self.new_detail_form.show()


