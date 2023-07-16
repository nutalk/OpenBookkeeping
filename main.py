from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QTableWidget,\
    QTableWidgetItem, QMenuBar, QMenu, QFileDialog, QStatusBar, QLabel
from PySide6.QtGui import QAction
from faker import Faker
from pathlib import Path

from OpenBookkeeping.main_window_center import MainTables
from OpenBookkeeping.new_prop import NewLiability, NewProp
from OpenBookkeeping.sql_db import init_db


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = None

        self.faker = Faker(locale='zh_CN')
        self.data = [[self.faker.name(), self.faker.address(), self.faker.ascii_free_email()] for _ in range(80)]

        self.resize(900, 700)
        self.setWindowTitle('财记')

        self.new_file_action = QAction('新建账本')
        self.openFile = QAction('打开账本')
        self.fileMenu = QMenu('文件')
        self.fileMenu.addAction(self.new_file_action)
        self.fileMenu.addAction(self.openFile)
        self.menuBar().addMenu(self.fileMenu)

        self.propAction = QAction('新增资产')
        self.liabilityAction = QAction('新增负债')
        self.propMenu = QMenu('新增账户')
        self.propMenu.addAction(self.propAction)
        self.propMenu.addAction(self.liabilityAction)
        self.menuBar().addMenu(self.propMenu)
        self.tables = MainTables()
        self.setCentralWidget(self.tables)

        self.new_prop_widget = None
        self.new_liability_widget = None

        self.band()
        self.update_status()

    def update_status(self):
        self.status_bar = QStatusBar()
        self.status_info = QLabel(f'账本文件: {self.database}')
        self.status_bar.addWidget(self.status_info)
        self.setStatusBar(self.status_bar)

        if self.database is None:
            self.propAction.setDisabled(True)
            self.liabilityAction.setDisabled(True)
        else:
            self.propAction.setDisabled(False)
            self.liabilityAction.setDisabled(False)
            if self.new_prop_widget is None:
                self.new_prop_widget = NewProp(self.database)
            if self.new_liability_widget is None:
                self.new_liability_widget = NewLiability(self.database)

    def band(self):
        self.propAction.triggered.connect(self.new_prop_fuc)
        self.liabilityAction.triggered.connect(self.new_liability_fuc)
        self.openFile.triggered.connect(self.open_db_fuc)
        self.new_file_action.triggered.connect(self.new_db_fuc)

    def new_db_fuc(self):
        file_dialog = QFileDialog(self)
        file_use = file_dialog.getSaveFileName(self, "新建文件", filter=".bp (*.bk)")
        init_db(file_use[0])
        self.database = file_use[0]
        self.update_status()

    def open_db_fuc(self):
        file_dialog = QFileDialog(self)
        file_use = file_dialog.getOpenFileName(self, "选择文件", filter=".bp (*.bk)")
        file_path = file_use[0]
        self.database = file_path
        self.update_status()

    def new_prop_fuc(self):
        self.new_prop_widget.show()
        self.update_status()

    def new_liability_fuc(self):
        self.new_liability_widget.show()
        self.update_status()


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()

    