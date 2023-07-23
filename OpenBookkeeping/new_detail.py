from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QDoubleSpinBox, QSpinBox, QComboBox, \
    QTextEdit, QDateEdit
from PySide6.QtCore import QDate
from loguru import logger

from OpenBookkeeping.new_prop import NewItem
from OpenBookkeeping.sql_db import add_detail, query_by_col


class NewDetail(NewItem):
    def __init__(self, database: str, parent: QWidget, table_name: str,
                 target_name: str, target_table_name: str):
        super().__init__(database, '记一笔', parent)
        self.table_name = table_name
        self.target_name = target_name
        rec = query_by_col(database, target_table_name, 'name', target_name)
        assert len(rec) == 1, f'记录不存在, {rec=}'
        self.target_id = rec[0][0]

        input_layout = QGridLayout()

        all_labels = dict(
            name=QLabel('名称'),
            start_date=QLabel('发生日期'),
            amount=QLabel('变化金额'),
            comment=QLabel('备注'),
        )

        self.all_input = dict(
            name=QLineEdit(),
            start_date=QDateEdit(),
            amount=QSpinBox(),
            comment=QTextEdit()
        )
        self.all_input['name'].setText(self.target_name)
        self.all_input['name'].setEnabled(False)
        self.all_input['start_date'].setDisplayFormat("yyyy-MM-dd")
        self.all_input['start_date'].setCalendarPopup(True)
        self.all_input['start_date'].setDate(QDate.currentDate())
        self.all_input['amount'].setMaximum(999999999)

        for idx, _label in enumerate(all_labels.values()):
            input_layout.addWidget(_label, idx + 1, 1)
        for idx, _input in enumerate(self.all_input.values()):
            input_layout.addWidget(_input, idx + 1, 2)

        input_layout.addWidget(self.warring_label, idx + 2, 2)
        input_layout.addLayout(self.buts_layout, idx + 3, 2)
        self.setLayout(input_layout)

    def get_data(self):
        start_date = self.all_input['start_date'].date().toString("yyyy-MM-dd")
        amount = self.all_input['amount'].value()
        comment = self.all_input['comment'].toPlainText()
        logger.debug(f'{amount=}, {start_date=} \
        {comment=}, {self.database}')
        return start_date, amount, comment

    def check_valid(self) -> str:
        start_date, amount, comment = self.get_data()
        add_detail(self.database, self.target_id, start_date, amount, comment, self.table_name)

