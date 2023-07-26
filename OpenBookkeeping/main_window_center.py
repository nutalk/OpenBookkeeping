from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem, QAction
from PySide6.QtCore import Qt, Signal
from loguru import logger

from OpenBookkeeping.sql_db import query_by_str, query_by_col
from OpenBookkeeping.gloab_info import query_liability_table, query_prop_table, \
    prop_type_items, liability_type_items, liability_currency_types, \
    prop_type_ids, liability_type_ids, liability_currency_ids
from OpenBookkeeping.new_prop import EditProp, EditLiability
from OpenBookkeeping.new_detail import NewDetail


class TableBase(QWidget):
    row_select_signal = Signal(str, str)

    def __init__(self, label_str, table_name: str):
        super().__init__()
        self.table_name = table_name
        self.edit_form = None
        self.database = None
        label = QLabel(label_str)
        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(label)
        self.setLayout(self.layout_main)
        self._table = QTableWidget()
        self.edit_action = QAction('编辑')
        self.edit_action.triggered.connect(self.on_edit)
        self.add_action = QAction('记一笔')
        self.add_action.triggered.connect(self.add_detail)
        # self.delete_action = QAction('删除')
        # self.delete_action.triggered.connect(self.on_delete)
        self._table.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self._table.addAction(self.edit_action)
        self._table.addAction(self.add_action)
        # self._table.addAction(self.delete_action)

        self._table.cellClicked.connect(self.select_line_emit)

    def select_line_emit(self):
        name_item = self.on_edit()
        self.row_select_signal.emit(self.table_name, name_item)

    def update_content(self, database: str, query_str: str):
        self.database = database
        props = query_by_str(database, query_str)
        self._table.setRowCount(len(props))
        return props

    def get_row_name(self) -> str:
        i = self._table.currentRow()
        name_item = self._table.item(i, 0)
        logger.debug(name_item.text())
        return name_item.text()

    def on_edit(self) -> tuple:
        row_name = self.get_row_name()
        rec = query_by_col(self.database, self.table_name, 'name', row_name)
        if len(rec) != 1:
            logger.error(f'{rec=}')
            raise ValueError('找不到匹配的数据')
        rec = rec[0]
        logger.debug(rec)
        return rec

    def on_delete(self) -> str:
        return self.get_row_name()

    def add_detail(self):
        return self.get_row_name()


class PropTable(TableBase):
    def __init__(self):
        super().__init__('资产汇总', 'prop')
        self._table.setRowCount(5)
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(['名称', '类别', '创建日期', '现金流', '余额'])

        self.layout_main.addWidget(self._table)

    def update_status(self):
        self.update_content(self.database, query_prop_table)

    def update_content(self, database: str, query_str: str):
        props = super().update_content(database, query_str)
        for row_id, prop in enumerate(props):
            for col_id, v in enumerate(prop):
                if col_id == 1:
                    v = prop_type_items[v]
                _item = QTableWidgetItem(str(v))
                self._table.setItem(row_id, col_id, _item)

    def on_edit(self):
        rec = super().on_edit()

        self.edit_form = EditProp(self.database, self)
        self.edit_form.set_values(rec[1],  rec[2], rec[3], rec[4], rec[5])
        self.edit_form.show()

    def add_detail(self):
        prop_name = self.get_row_name()
        self.add_detail_form = NewDetail(self.database, self, 'prop_details', prop_name, 'prop')
        self.add_detail_form.show()


class LiabilityTable(TableBase):
    def __init__(self):
        super().__init__('负债汇总', 'liability')
        self._table.setRowCount(5)
        self._table.setColumnCount(7)
        # name, type, currency_type, start_date, term_month, rate, sum(amount) 
        self._table.setHorizontalHeaderLabels(['名称', '类别', '还款方式', '开始日期', '期限', '利率', '余额'])

        self.layout_main.addWidget(self._table)

    def update_status(self):
        self.update_content(self.database, query_liability_table)

    def update_content(self, database: str, query_str: str):
        liabilities = super().update_content(database, query_str)
        for row_id, liability in enumerate(liabilities):
            for col_id, v in enumerate(liability):
                if col_id == 1:
                    v = liability_type_items[v]
                elif col_id == 2:
                    v = liability_currency_types[v]
                _item = QTableWidgetItem(str(v))
                self._table.setItem(row_id, col_id, _item)

    def on_edit(self):
        rec = super().on_edit()

        self.edit_form = EditLiability(self.database, self)
        self.edit_form.set_values(rec[1],  rec[2], rec[3], rec[4], rec[5], rec[6], rec[7])
        self.edit_form.show()

    def add_detail(self):
        prop_name = self.get_row_name()
        self.add_detail_form = NewDetail(self.database, self, 'liability_details', prop_name, 'liability')
        self.add_detail_form.show()


class MainTables(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.prop_table = PropTable()
        self.liability_table = LiabilityTable()
        left_layout.addWidget(self.prop_table)
        left_layout.addWidget(self.liability_table)

        right_btns_layout = QHBoxLayout()
        add_detail_btn = QPushButton('记一笔')
        edit_detail_btn = QPushButton('编辑')
        del_detail_btn = QPushButton('删除')
        right_btns_layout.addWidget(add_detail_btn)
        right_btns_layout.addWidget(edit_detail_btn)
        right_btns_layout.addWidget(del_detail_btn)

        self.detail_table = QTableWidget()
        self.detail_table.setRowCount(10)
        self.detail_table.setColumnCount(5)
        self.detail_table.setHorizontalHeaderLabels(['账户名称', '日期', '金额', '余额', '备注'])

        right_layout.addWidget(self.detail_table)
        right_layout.addLayout(right_btns_layout)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        self.prop_table.row_select_signal.connect(self.update_detail)

    def update_content(self, database:str):
        self.prop_table.update_content(database, query_prop_table)
        self.liability_table.update_content(database, query_liability_table)

    def update_detail(self, *args, **kwargs):
        logger.debug(args)

