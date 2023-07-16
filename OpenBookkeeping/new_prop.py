from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton,\
    QHBoxLayout, QVBoxLayout, QGridLayout, QDoubleSpinBox, QSpinBox, QComboBox


class NewProp(QWidget):
    def __init__(self, database: str):
        super().__init__()
        self.database = database

        self.setWindowTitle('新增资产')
        input_layout = QGridLayout()
        name_label = QLabel('名称')
        type_label = QLabel('类别')
        rate_label = QLabel('年利率')
        currency_label = QLabel('月现金流')

        self.name_input = QLineEdit()
        items = ['固定资产', '流动资产']
        self.type_input = QComboBox()
        self.type_input.addItems(items)
        self.rate_input = QDoubleSpinBox()
        self.currency_input = QSpinBox()
        self.currency_input.setMaximum(999999999)

        input_layout.addWidget(name_label, 1, 1)
        input_layout.addWidget(type_label, 2, 1)
        input_layout.addWidget(rate_label, 3, 1)
        input_layout.addWidget(currency_label, 4, 1)

        input_layout.addWidget(self.name_input, 1, 2)
        input_layout.addWidget(self.type_input, 2, 2)
        input_layout.addWidget(self.rate_input, 3, 2)
        input_layout.addWidget(self.currency_input, 4,2)

        buts_layout = QHBoxLayout()
        self.cancel_btn = QPushButton('取消')
        self.confirm_btn = QPushButton('确定')
        buts_layout.addWidget(self.cancel_btn)
        buts_layout.addWidget(self.confirm_btn)

        input_layout.addLayout(buts_layout, 5, 2)
        self.setLayout(input_layout)


class NewLiability(QWidget):
    def __init__(self, database: str):
        super().__init__()
        self.database = database
        self.setWindowTitle('新增负债')
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

        buts_layout = QHBoxLayout()
        self.cancel_btn = QPushButton('取消')
        self.confirm_btn = QPushButton('确定')
        buts_layout.addWidget(self.cancel_btn)
        buts_layout.addWidget(self.confirm_btn)

        input_layout.addLayout(buts_layout, 5, 2)
        self.setLayout(input_layout)