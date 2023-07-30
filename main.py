from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QTableWidget,\
    QTableWidgetItem, QMenuBar, QMenu, QFileDialog, QStatusBar, QLabel
from PySide6.QtGui import QAction

from pathlib import Path

from OpenBookkeeping.main_window_center import MainLayouts
from OpenBookkeeping.sql_db import init_db


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = None

        self.resize(1080, 700)
        self.setWindowTitle('财记')

        self.new_file_action = QAction('新建账本')
        self.openFile = QAction('打开账本')
        self.fileMenu = QMenu('文件')
        self.fileMenu.addAction(self.new_file_action)
        self.fileMenu.addAction(self.openFile)
        self.menuBar().addMenu(self.fileMenu)

        self.propMenu = QMenu('账户管理')
        self.menuBar().addMenu(self.propMenu)

        self.check_action = QMenu('对账')
        self.menuBar().addMenu(self.check_action)

        self.pred_action = QMenu('预测')
        self.menuBar().addMenu(self.pred_action)

        self.tables = MainLayouts()
        self.setCentralWidget(self.tables)

        self.new_prop_widget = None
        self.new_liability_widget = None

    def new_db_fuc(self):
        file_dialog = QFileDialog(self)
        file_use = file_dialog.getSaveFileName(self, "新建文件", filter=".bk (*.bk)")
        init_db(file_use[0])
        self.database = file_use[0]

    def open_db_fuc(self):
        file_dialog = QFileDialog(self)
        file_use = file_dialog.getOpenFileName(self, "选择文件", filter=".bk (*.bk)")
        file_path = file_use[0]
        self.database = file_path

    def new_prop_fuc(self):
        self.new_prop_widget.show()

    def new_liability_fuc(self):
        self.new_liability_widget.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()

    