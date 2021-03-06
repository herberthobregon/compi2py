import sys
import os, subprocess
from PyQt5 import QtWidgets, QtCore, QtGui
from ui.main_ui import Ui_MainWindow
from ui import code_editor_minor_c as minor_c
from ui import code_editor as angus_editor
from typing import List
from compi.gramaticas import globales
from compi.MinorC import globales2

from run_angus import get_ast, debug_ast, step
import run_minor_c


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.print_outs = 0
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.editors: List[List[minor_c.QCodeEditor]] = []
        self.add_tab()
        self.console = ''

    def add_tab(self):
        container = QtWidgets.QWidget()
        container.setObjectName("tab_3")
        text_edit = minor_c.QCodeEditor(container)
        text_edit2 = angus_editor.QCodeEditor(container)
        text_edit.setGeometry(QtCore.QRect(10, 10, 521, 361))
        text_edit2.setGeometry(QtCore.QRect(550, 10, 521, 361))
        text_edit.setObjectName("textEdit_{}".format(self.ui.tabWidget.count()))
        font = QtGui.QFont()
        font.setFamily("Monaco")
        text_edit.setFont(font)
        text_edit2.setFont(font)

        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(248, 248, 242))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)

        brush = QtGui.QBrush(QtGui.QColor(39, 40, 34))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)

        # text_edit.setPalette(palette)
        self.editors.append([text_edit, text_edit2])

        self.ui.tabWidget.addTab(container, '')
        # for i in range(self.ui.tabWidget.count()):
        self.ui.tabWidget.setTabText(self.ui.tabWidget.count() - 1, "Untitled-{}".format(self.ui.tabWidget.count()))

        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

    def close_current_tab(self):
        index = self.ui.tabWidget.currentIndex()
        count = self.ui.tabWidget.count() - 1
        if count > 0:
            self.ui.tabWidget.removeTab(index)
            del self.editors[index]

    def on_close_tab(self, index: int):
        count = self.ui.tabWidget.count() - 1
        if count > 0:
            self.ui.tabWidget.removeTab(index)
            del self.editors[index]

    # ====================================== debug ======================================
    def debug(self):
        index = self.ui.tabWidget.currentIndex()
        txt = self.editors[index][1].toPlainText()
        if len(txt) > 2:
            def println(t: str):
                self.print(t)

            root = debug_ast(txt, self, println)
            self.ui.lb_debug_active.setText('TRUE')
            self.ui.debugline.setText(str(root.line))

    def step(self):
        root = step()
        self.ui.debugline.setText(str(root.line))

    def stop_debug(self):
        root = step()
        self.ui.debugline.setText(str(root.line))

    def stop_run(self):
        self.ui.debugline.setText(str(0))
        self.ui.lb_debug_active.setText('false')

    # //====================================== debug ======================================

    # ====================================== Files ======================================
    def open_file(self):
        dirr = QtCore.QDir()
        qfile = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", dirr.absoluteFilePath("."), "Files (*.*)")
        if len(qfile[0]) == 0:
            return
        file = QtCore.QFile(qfile[0])
        file.open(QtCore.QFile.ReadOnly)
        filename = file.fileName()
        txt = str(file.readAll().data(), encoding='utf-8')
        index = self.ui.tabWidget.currentIndex()
        parts = filename.split("/")

        self.editors[index][0].path = filename
        self.editors[index][0].filename = parts[len(parts) - 1]

        self.editors[index][0].setPlainText(txt)
        self.ui.tabWidget.setTabText(index, self.editors[index][0].filename)
        self.ui.tabWidget.setTabToolTip(self.ui.tabWidget.count() - 1, filename)

    def save_file(self):
        dirr = QtCore.QDir()
        index = self.ui.tabWidget.currentIndex()
        code_editor = self.editors[index][0]
        if code_editor.path == "":
            qfile = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", dirr.absoluteFilePath('.'), "OLC2 Files (*.txt)")
            if len(qfile[0]) == 0:
                return
            parts = qfile[0].split("/")
            code_editor.path = qfile[0]
            code_editor.filename = parts[len(parts) - 1]

        self.ui.tabWidget.setTabText(index, code_editor.filename)
        file = open(code_editor.path, 'w')
        file.write(code_editor.toPlainText())
        file.close()

    def save_as(self):
        index = self.ui.tabWidget.currentIndex()
        code_editor = self.editors[index][0]
        qfile = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", QtCore.QDir.homePath(), "OLC2 Files (*.txt)")
        if len(qfile[0]) == 0:
            return
        code_editor.path = qfile[0]
        file = open(code_editor.path, 'w')
        file.write(code_editor.toPlainText())
        file.close()

    # //====================================== Files ======================================

    def run_desc(self):
        index = self.ui.tabWidget.currentIndex()
        txt = self.editors[index][1].toPlainText()
        if len(txt) > 2:
            def println(t: str):
                self.print(t)

            root = get_ast(txt, self, println)

    def run_convert(self):
        index = self.ui.tabWidget.currentIndex()
        txt = self.editors[index][0].toPlainText()

        if len(txt) > 2:
            def println(t: str):
                self.print(t)

            root = run_minor_c.get_ast(txt, self, println)
            self.editors[index][1].setPlainText(root)

    def run_asc(self):
        pass

    # //====================================== Reports Angus ======================================
    def report_errors(self):
        path = os.getcwd() + '/report_angus_errores.html'
        file = open(path, 'w')
        rows = ['<tr><th>Type</th><th>Line</th><th>Col</th><th>descrip</th></tr>']
        for el in globales.lErroresSemanticos:
            rows.append('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(el.t, el.line, el.col, el.decrip))

        for el in globales.lErrores:
            rows.append('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(el.t, el.line, el.col, el.decrip))
        html = """
                    <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Tabla de simbolos</title>
                <style>
            table {{
              font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              width: 100%;
              max-width: 500px;
            margin: 0 auto;
            }}

            table td, table th {{
              border: 1px solid #ddd;
              padding: 8px;
            }}

            table tr:nth-child(even){{background-color: #f2f2f2;}}

            table tr:hover {{background-color: #ddd;}}

            table th {{
              padding-top: 12px;
              padding-bottom: 12px;
              text-align: left;
              background-color: #4CAF50;
              color: white;
            }}
            </style>
            </head>
            <body>
            <table>
                {}
            </table>
            </body>
            </html>
                    """.format('\n'.join(rows))
        file.write(html)
        file.close()
        subprocess.Popen(["open", path])

    def report_var_table(self):
        path = os.getcwd() + '/report_angus_functions.html'
        file = open(path, 'w')
        rows = ['<tr><th>Function</th><th>Type</th></tr>']
        for key in globales.all_tags:
            rows.append('<tr><td>{}</td><td>{}</td></tr>'.format(key, globales.all_tags[key].typee))
        html = """
            <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tabla de simbolos</title>
        <style>
    table {{
      font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
      border-collapse: collapse;
      width: 100%;
      max-width: 500px;
    margin: 0 auto;
    }}

    table td, table th {{
      border: 1px solid #ddd;
      padding: 8px;
    }}

    table tr:nth-child(even){{background-color: #f2f2f2;}}

    table tr:hover {{background-color: #ddd;}}

    table th {{
      padding-top: 12px;
      padding-bottom: 12px;
      text-align: left;
      background-color: #4CAF50;
      color: white;
    }}
    </style>
    </head>
    <body>
    <table>
        {}
    </table>
    </body>
    </html>
            """.format('\n'.join(rows))
        file.write(html)
        file.close()
        subprocess.Popen(["open", path])

    def report_sym_tab(self):
        path = os.getcwd() + '/report_angus_sym.html'
        file = open(path, 'w')
        rows = ['<tr><th>Key</th><th>Value</th></tr>']
        for i in globales.sym_table:
            rows.append('<tr><td>{}</td><td>{}</td></tr>'.format(i.key, str(i.value)))
        html = """
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tabla de simbolos</title>
    <style>
table {{
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
  max-width: 500px;
margin: 0 auto;
}}

table td, table th {{
  border: 1px solid #ddd;
  padding: 8px;
}}

table tr:nth-child(even){{background-color: #f2f2f2;}}

table tr:hover {{background-color: #ddd;}}

table th {{
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #4CAF50;
  color: white;
}}
</style>
</head>
<body>
<table>
    {}
</table>
</body>
</html>
        """.format('\n'.join(rows))
        file.write(html)
        file.close()
        subprocess.Popen(["open", path])

    def report_ast(self):
        path = os.getcwd() + '/report_angus_graph.svg'
        subprocess.Popen(["open", path])

    # //====================================== Reports Aguns ======================================

    # //====================================== Reports MinorC ======================================
    def report_errors_minorc(self):
        path = os.getcwd() + '/report_minorc_errores.html'
        file = open(path, 'w')
        rows = ['<tr><th>Type</th><th>Line</th><th>Col</th><th>descrip</th></tr>']
        for el in globales2.lErroresSemanticos:
            rows.append('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(el.t, el.line, el.col, el.decrip))

        for el in globales2.lErrores:
            rows.append('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(el.t, el.line, el.col, el.decrip))
        html = """
                    <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Tabla de simbolos</title>
                <style>
            table {{
              font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              width: 100%;
              max-width: 500px;
            margin: 0 auto;
            }}

            table td, table th {{
              border: 1px solid #ddd;
              padding: 8px;
            }}

            table tr:nth-child(even){{background-color: #f2f2f2;}}

            table tr:hover {{background-color: #ddd;}}

            table th {{
              padding-top: 12px;
              padding-bottom: 12px;
              text-align: left;
              background-color: #4CAF50;
              color: white;
            }}
            </style>
            </head>
            <body>
            <table>
                {}
            </table>
            </body>
            </html>
                    """.format('\n'.join(rows))
        file.write(html)
        file.close()
        subprocess.Popen(["open", path])

    def report_var_table_minorc(self):
        path = os.getcwd() + '/report_minorc_functions.html'
        file = open(path, 'w')
        rows = ['<tr><th>Function</th><th>Type</th></tr>']
        for i in globales2.r_shiftreduce_grammar:
            rows.append('<tr><td>{}</td><td>{}</td></tr>'.format(i[0], str(i[1])))
        html = """
            <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tabla de simbolos</title>
        <style>
    table {{
      font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
      border-collapse: collapse;
      width: 100%;
      max-width: 500px;
    margin: 0 auto;
    }}

    table td, table th {{
      border: 1px solid #ddd;
      padding: 8px;
    }}

    table tr:nth-child(even){{background-color: #f2f2f2;}}

    table tr:hover {{background-color: #ddd;}}

    table th {{
      padding-top: 12px;
      padding-bottom: 12px;
      text-align: left;
      background-color: #4CAF50;
      color: white;
    }}
    </style>
    </head>
    <body>
    <table>
        {}
    </table>
    </body>
    </html>
            """.format('\n'.join(rows))
        file.write(html)
        file.close()
        subprocess.Popen(["open", path])

    def report_sym_tab_minorc(self):
        path = os.getcwd() + '/report_minorc_sym.html'
        file = open(path, 'w')
        rows = ['<tr><th>Key</th><th>Value</th></tr>']
        for i in globales2.sym_table:
            rows.append('<tr><td>{}</td><td>{}</td></tr>'.format(i.key, str(i.value)))
        html = """
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tabla de simbolos</title>
    <style>
table {{
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
  max-width: 500px;
margin: 0 auto;
}}

table td, table th {{
  border: 1px solid #ddd;
  padding: 8px;
}}

table tr:nth-child(even){{background-color: #f2f2f2;}}

table tr:hover {{background-color: #ddd;}}

table th {{
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #4CAF50;
  color: white;
}}
</style>
</head>
<body>
<table>
    {}
</table>
</body>
</html>
        """.format('\n'.join(rows))
        file.write(html)
        file.close()
        subprocess.Popen(["open", path])

    def report_sym_tab_fun_minorc(self):
        path = os.getcwd() + '/report_minorc_sym_fun.html'
        file = open(path, 'w')
        rows = ['<tr><th>Funcion</th><th>Line</th></tr>']
        for i in globales2.sym_table_fun:
            rows.append('<tr><td>{}</td><td>{}</td></tr>'.format(i.key, str(i.line)))
        html = """
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tabla de simbolos Funciones</title>
    <style>
table {{
  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
  border-collapse: collapse;
  width: 100%;
  max-width: 500px;
margin: 0 auto;
}}

table td, table th {{
  border: 1px solid #ddd;
  padding: 8px;
}}

table tr:nth-child(even){{background-color: #f2f2f2;}}

table tr:hover {{background-color: #ddd;}}

table th {{
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #4CAF50;
  color: white;
}}
</style>
</head>
<body>
<table>
    {}
</table>
</body>
</html>
        """.format('\n'.join(rows))
        file.write(html)
        file.close()
        subprocess.Popen(["open", path])

    def report_ast_minorc(self):
        path = os.getcwd() + '/report_minorc_graph.svg'
        subprocess.Popen(["open", path])

    # //====================================== Reports MinorC ======================================

    def print(self, txt: str):
        print("> {}".format(txt))
        self.print_outs += 1
        out = "{}> {}\n".format(self.console, txt)
        self.console = out
        self.ui.teConsole.setPlainText(str(self.console))
        self.ui.teConsole.verticalScrollBar().setSliderPosition(self.ui.teConsole.verticalScrollBar().maximum())


def get_doc(imported_module):
    _items = [(k, getattr(imported_module, k)) for k in dir(imported_module)]
    pdict = dict(_items)
    gramar = []
    for key in pdict:
        if key.startswith('p_'):
            gramar.append(pdict[key].__doc__)
    return "\n\n".join([d if d else '' for d in gramar])


app = QtWidgets.QApplication(sys.argv)
mainWindow = MainWindow()
sys.exit(app.exec_())
