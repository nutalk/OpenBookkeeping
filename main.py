from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QTableWidget,\
    QTableWidgetItem, QMenuBar, QMenu
from PySide6.QtGui import QAction
from faker import Faker


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.faker = Faker(locale='zh_CN')
        self.data = [[self.faker.name(), self.faker.address(), self.faker.ascii_free_email()] for _ in range(80)]

        self.resize(900, 700)

        self.setWindowTitle('财记')
        self.openFile = QAction('打开账本')
        self.closeFile = QAction('关闭账本')
        self.saveFile = QAction('保存账本')

        self.fileMenu = QMenu('文件')
        self.fileMenu.addAction(self.openFile)
        self.fileMenu.addAction(self.closeFile)

        self.menuBar().addMenu(self.fileMenu)

        self.table = QTableWidget()
        self.table.setRowCount(10)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['姓名', '地址', 'Email Address'])
        # self.table.setVerticalHeaderLabels(['A', 'B', 'C'])
        self.layout().addWidget(self.table)

        # self.setLayout(self.mainLayout)


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()