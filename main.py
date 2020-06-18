import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from ui.main_ui import Ui_MainWindow
from ui.code_editor2 import QCodeEditor
# from ui.code_editor import CodeEditor 272822
from typing import List


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.editors: List[QCodeEditor] = []
        self.add_tab()

    def add_tab(self):
        text_edit = QCodeEditor()
        text_edit.setGeometry(QtCore.QRect(10, 10, 731, 361))
        text_edit.setObjectName("textEdit_{}".format(self.ui.tabWidget.count()))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        text_edit.setFont(font)

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(118, 252, 123))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)

        brush = QtGui.QBrush(QtGui.QColor(39, 40, 34))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

        text_edit.setPalette(palette)
        self.editors.append(text_edit)

        self.ui.tabWidget.addTab(text_edit, '')
        for i in range(self.ui.tabWidget.count()):
            self.ui.tabWidget.setTabText(i, "Tab {}".format(i + 1))

        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

    def close_current_tab(self):
        index = self.ui.tabWidget.currentIndex()
        count = self.ui.tabWidget.count() - 1
        if count > 0:
            self.ui.tabWidget.removeTab(index)
            del self.editors[index]

    def debug(self):
        pass

    def on_close_tab(self, index: int):
        count = self.ui.tabWidget.count() - 1
        if count > 0:
            self.ui.tabWidget.removeTab(index)
            del self.editors[index]

    def run_desc(self):
        index = self.ui.tabWidget.currentIndex()
        txt = self.editors[index].toPlainText()
        print(txt)

    def run_asc(self):
        index = self.ui.tabWidget.currentIndex()
        txt = self.editors[index].toPlainText()
        print(txt)

    def stop_run(self):
        pass

    def open_file(self):
        qfile = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", QtCore.QDir.homePath(), "Files (*.*)")
        if len(qfile[0]) == 0:
            return
        file = QtCore.QFile(qfile[0])
        file.open(QtCore.QFile.ReadOnly)
        filename = file.fileName()
        txt = str(file.readAll().data(), encoding='utf-8')
        index = self.ui.tabWidget.currentIndex()
        self.editors[index].setPlainText(txt)

    def save_file(self):
        index = self.ui.tabWidget.currentIndex()
        code_editor = self.editors[index]
        if code_editor.path:
            pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
