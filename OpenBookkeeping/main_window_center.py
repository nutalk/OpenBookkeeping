from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, \
    QHBoxLayout, QVBoxLayout, QPushButton


class MainTables(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_btns_layout = QHBoxLayout()
        edit_prop_btn = QPushButton('编辑')
        del_prop_btn = QPushButton('删除')
        left_btns_layout.addWidget(edit_prop_btn)
        left_btns_layout.addWidget(del_prop_btn)

        self.prop_table = QTableWidget()
        self.prop_table.setRowCount(10)
        self.prop_table.setColumnCount(4)
        self.prop_table.setHorizontalHeaderLabels(['类别', '名称', '余额', '现金流'])

        left_layout.addWidget(self.prop_table)
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
