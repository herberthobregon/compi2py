from PyQt5 import QtCore, QtGui, QtWidgets


class CodeEditor(QtWidgets.QPlainTextEdit):
    def __init__(self, q_widget: QtWidgets.QPlainTextEdit):
        super().__init__(q_widget)
        self.line_number_area = LineNumberArea(self)



class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, code_editor: CodeEditor):
        super().__init__(self)
