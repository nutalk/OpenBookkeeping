from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton,\
    QHBoxLayout, QVBoxLayout, QGridLayout, QDoubleSpinBox, QSpinBox, QComboBox, \
    QTextEdit

from OpenBookkeeping.sql_db import add_prop


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
        name_label = QLabel('名称')
        type_label = QLabel('类别')
        currency_label = QLabel('月现金流')
        comment_label = QLabel('备注')

        self.name_input = QLineEdit()
        items = ['固定资产', '流动资产']
        self.type_input = QComboBox()
        self.type_input.addItems(items)
        self.currency_input = QSpinBox()
        self.currency_input.setMaximum(999999999)
        self.comment_input = QTextEdit()

        input_layout.addWidget(name_label, 1, 1)
        input_layout.addWidget(type_label, 2, 1)
        input_layout.addWidget(currency_label, 3, 1)
        input_layout.addWidget(comment_label, 4, 1)

        input_layout.addWidget(self.name_input, 1, 2)
        input_layout.addWidget(self.type_input, 2, 2)
        input_layout.addWidget(self.currency_input, 3, 2)
        input_layout.addWidget(self.comment_input, 4, 2)

        input_layout.addWidget(self.warring_label, 5, 2)
        input_layout.addLayout(self.buts_layout, 6, 2)
        self.setLayout(input_layout)

    def check_valid(self) -> str:
        prop_name = self.name_input.text()
        prop_type = self.type_input.currentIndex()
        currency = self.currency_input.value()
        comment = self.comment_input.toPlainText()
        print(f'{prop_name=}, {prop_type=}, {currency=}, {comment=}')

        add_prop(self.database, str(prop_name), int(prop_type),
                 int(currency), str(comment))


class NewLiability(NewItem):
    def __init__(self, database: str):
        super().__init__(database, '新增负债')
        input_layout = QGridLayout()
        name_label = QLabel('名称')
        type_label = QLabel('负债类型')
        currency_label = QLabel('还款付息类型')
        rate_label = QLabel('年利率')

        self.name_input = QLineEdit()
        self.type_input = QComboBox()
        self.type_input.addItems(['长期负债', '短期负债'])
        self.currency_type_input = QComboBox()
        self.currency_type_input.addItems(['先息后本', '等额本息', '等额本金', '到期还本付息'])
        self.rate_input = QDoubleSpinBox()

        input_layout.addWidget(name_label, 1, 1)
        input_layout.addWidget(type_label, 2, 1)
        input_layout.addWidget(currency_label, 3, 1)
        input_layout.addWidget(rate_label, 4, 1)

        input_layout.addWidget(self.name_input, 1, 2)
        input_layout.addWidget(self.type_input, 2, 2)
        input_layout.addWidget(self.currency_type_input, 3,2)
        input_layout.addWidget(self.rate_input, 4, 2)
        input_layout.addWidget(self.warring_label, 5, 2)
        input_layout.addLayout(self.buts_layout, 6, 2)
        self.setLayout(input_layout)