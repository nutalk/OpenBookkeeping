from PySide6.QtWidgets import QTreeView, QWidget, QHBoxLayout, QApplication
from PySide6.QtGui import QStandardItemModel, QStandardItem
from collections import defaultdict


class TreeView(QWidget):
    def __init__(self):
        super().__init__()
        self.tree = QTreeView(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.tree)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['类别', '名称', '余额'])
        # self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)

        self.setLayout(layout)

    def adj_data(self, data: dict):
        root = self.model.invisibleRootItem()
        for type_id, rec_dict in data.items():
            child_type = QStandardItem(str(type_id))
            child_name = QStandardItem('')
            child_amount = QStandardItem(str(rec_dict['amount']))
            root.appendRow([child_type, child_name, child_amount])
            for rec in rec_dict['recs']:
                child_type.appendRow([
                        QStandardItem(str(v)) for v in rec
                    ])
        self.tree.expandAll()


def trans_data(data: list) -> dict:
    data_rec = {}
    for rec in data:
        type_id, name, amount = rec
        if data_rec.get(type_id) is None:
            data_rec[type_id] = {'amount': amount, 'recs': [rec]}
        else:
            data_rec[type_id]['amount'] += amount
            data_rec[type_id]['recs'].append(rec)
    return data_rec


if __name__ == '__main__':
    data = [(0, '2b801', 5),
            (0, '42001', 7),
            (1, 'zs', 1),
            (1, 'zh', 2)]
    data_trans = trans_data(data)

    app = QApplication([])
    window = TreeView()
    window.adj_data(data_trans)
    window.show()
    app.exec()
