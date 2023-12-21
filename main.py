from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QTableWidget,\
    QTableWidgetItem, QMenuBar, QMenu, QFileDialog, QStatusBar, QLabel, QTabWidget
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from functools import wraps
from pathlib import Path
from loguru import logger

from OpenBookkeeping.main_window_detail import DetailPage
from OpenBookkeeping.sql_db import init_db
from OpenBookkeeping.new_prop import NewProp


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.database = None
        self.resize(1280, 700)
        self.setWindowTitle('财记')

        self.new_file_action = QAction('新建账本')
        self.openFile = QAction('打开账本')
        self.fileMenu = QMenu('文件')
        self.fileMenu.addAction(self.new_file_action)
        self.fileMenu.addAction(self.openFile)
        self.menuBar().addMenu(self.fileMenu)

        self.propMenu = QAction('账户管理')
        self.menuBar().addAction(self.propMenu)

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.tabBarClicked.connect(self.update_content)
        self.detail_widget = DetailPage()
        self.tab_widget.addTab(self.detail_widget, '明细')

        self.new_prop_widget = None
        self.new_liability_widget = None
        self.band()

    @property
    def ready(self):
        if self.database is not None:
            database = Path(self.database)
            if database.is_file() and database.exists():
                return True

        return False

    def update_content(self):
        if self.ready:
            self.propMenu.setEnabled(True)
            self.tab_widget.setEnabled(True)
            self.detail_widget.update_content(self.database)
        else:
            self.propMenu.setEnabled(False)
            self.tab_widget.setEnabled(False)

    def update_after(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            self.update_content()
            return res

        return wrapper

    @update_after
    def band(self):
        self.openFile.triggered.connect(self.open_db_fuc)
        self.new_file_action.triggered.connect(self.new_db_fuc)
        self.propMenu.triggered.connect(self.edit_prop)

    @update_after
    def new_db_fuc(self):
        file_dialog = QFileDialog(self)
        file_use = file_dialog.getSaveFileName(self, "新建文件", filter=".bk (*.bk)")
        init_db(file_use[0])
        self.database = file_use[0]

    @update_after
    def open_db_fuc(self):
        file_dialog = QFileDialog(self)
        file_use = file_dialog.getOpenFileName(self, "选择文件", filter=".bk (*.bk)")
        file_path = file_use[0]
        self.database = file_path

    @update_after
    def edit_prop(self):
        # TODO 在编辑之后应该更新界面
        logger.debug(f'edit prop')
        self.prop_window = NewProp(self.database)
        self.prop_window.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()

    