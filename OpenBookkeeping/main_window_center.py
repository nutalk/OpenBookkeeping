from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTableView
from PySide6.QtGui import QStandardItemModel, QStandardItem


class TableBase(QWidget):
    def __init__(self, label_str):
        super().__init__()
        label = QLabel(label_str)
        self.layout_main = QVBoxLayout()
        self.layout_main.addWidget(label)
        self.setLayout(self.layout_main)

    def update_data(self, new_data: list):
        ...


class PropTable(TableBase):
    def __init__(self):
        super().__init__('资产汇总')

        self._table = QTableWidget()
        self._table.setRowCount(5)
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(['类别', '名称', '余额', '现金流', '创建日期'])

        self.layout_main.addWidget(self._table)


class LiabilityTable(TableBase):
    def __init__(self):
        super().__init__('负债汇总')
        self._table = QTableWidget()
        self._table.setRowCount(5)
        self._table.setColumnCount(7)
        self._table.setHorizontalHeaderLabels(['类别', '名称', '余额', '利率', '开始日期', '期限', '现金流'])

        self.layout_main.addWidget(self._table)


class MainTables(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_btns_layout = QHBoxLayout()
        edit_prop_btn = QPushButton('编辑账户')
        left_btns_layout.addWidget(edit_prop_btn)

        self.prop_table = PropTable()
        self.liability_table = LiabilityTable()
        left_layout.addWidget(self.prop_table)
        left_layout.addWidget(self.liability_table)
        left_layout.addLayout(left_btns_layout)

        right_layout = QVBoxLayout()
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
