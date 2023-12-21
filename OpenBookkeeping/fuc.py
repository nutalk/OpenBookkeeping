from PySide6.QtCore import QDate, Signal, QAbstractTableModel, Qt
from loguru import logger
from collections import defaultdict


class DetailTableModel(QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self._data = []
        self._header = []

    def get_row(self, row_idx: int) -> tuple:
        return self._data[row_idx]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        if len(self._data) == 0:
            return 0
        else:
            return len(self._data[0])

    def update_content(self, data: list, header: list):
        self._data = data
        self._header = header

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self._header[section]

