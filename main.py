import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from ui.main_ui import Ui_MainWindow
from typing import List


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.editors: List[QtWidgets.QTextEdit] = [self.ui.teEditor1, self.ui.teEditor2]

    def add_tab(self):
        tab1 = QtWidgets.QWidget()
        tab1.setObjectName("tab")
        self.ui.tabWidget.addTab(tab1, '')
        for i in range(self.ui.tabWidget.count()):
            self.ui.tabWidget.setTabText(i, "Tab {}".format(i + 1))

        text_edit = QtWidgets.QTextEdit(tab1)
        text_edit.setGeometry(QtCore.QRect(10, 10, 731, 361))
        text_edit.setObjectName("textEdit_{}".format(self.ui.tabWidget.count()))
        self.editors.append(text_edit)

        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

    def on_close_tab(self, index: int):
        count = self.ui.tabWidget.count() - 1
        if count > 0:
            self.ui.tabWidget.removeTab(index)
            del self.editors[index]

    def run(self):
        index = self.ui.tabWidget.currentIndex()
        txt = self.editors[index].toPlainText()
        print(txt)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
