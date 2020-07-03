import PyQt5 as PyQt
from PyQt5.QtCore import Qt, QRect, QRegExp
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit
from PyQt5.QtGui import (
    QColor,
    QPainter,
    QFont,
    QSyntaxHighlighter,
    QTextFormat,
    QTextCharFormat
)


def index_of(text: str, search: str, fromm: int = 0):
    try:
        return text.index(search, fromm)
    except:
        return -1


class XMLHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):

        super(XMLHighlighter, self).__init__(parent)

        # numbers
        numbers = QTextCharFormat()
        numbers.setForeground(QColor("#ae81ff"))

        # comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#88846f"))

        green = QTextCharFormat()
        green.setForeground(QColor("#a6e22e"))

        morado = QTextCharFormat()
        morado.setForeground(QColor("#ae81ff"))

        # magenta
        magenta = QTextCharFormat()
        magenta.setForeground(QColor("#f92672"))

        # turquesa
        turquesa = QTextCharFormat()
        turquesa.setForeground(QColor("#66d9ef"))

        # orange
        orange = QTextCharFormat()
        orange.setForeground(QColor("#fd971f"))

        # bold
        bold = QTextCharFormat()
        bold.setFontWeight(QFont.Bold)

        # strings
        strings = QTextCharFormat()
        strings.setForeground(QColor("#e6db74"))

        self.highlightingRules = [
            [QRegExp(r"\b[0-9]+\.?[0-9]*\b"), numbers],
            [QRegExp(r"//[^\n]*"), comment_format],
            [QRegExp(r"\bchar\b"), turquesa], [QRegExp(r"\bclass\b"), magenta], [QRegExp(r"\bconst\b"), magenta],
            [QRegExp(r"\bdouble\b"), turquesa], [QRegExp(r"\benum\b"), turquesa], [QRegExp(r"\bexplicit\b"), magenta],
            [QRegExp(r"\bfriend\b"), magenta], [QRegExp(r"\binline\b"), magenta], [QRegExp(r"\bint\b"), turquesa],
            [QRegExp(r"\blong\b"), turquesa], [QRegExp(r"\bnamespace\b"), magenta], [QRegExp(r"\boperator\b"), magenta],
            [QRegExp(r"\bprivate\b"), magenta], [QRegExp(r"\bprotected\b"), magenta], [QRegExp(r"\bpublic\b"), magenta],
            [QRegExp(r"\bshort\b"), turquesa], [QRegExp(r"\bsignals\b"), magenta], [QRegExp(r"\bsigned\b"), magenta],
            [QRegExp(r"\bslots\b"), magenta], [QRegExp(r"\bstatic\b"), magenta], [QRegExp(r"\bstruct\b"), turquesa],
            [QRegExp(r"\btemplate\b"), magenta], [QRegExp(r"\btypedef\b"), magenta], [QRegExp(r"\btypename\b"), magenta],
            [QRegExp(r"\bunion\b"), magenta], [QRegExp(r"\bunsigned\b"), magenta], [QRegExp(r"\bvirtual\b"), magenta],
            [QRegExp(r"\bvoid\b"), turquesa], [QRegExp(r"\bvolatile\b"), magenta], [QRegExp(r"\bbool\b"), magenta],
            [QRegExp(r"\bnew\b"), magenta], [QRegExp(r"\b[A-Za-z0-9_]+(?=\()"), green], [QRegExp(r"<.*>"), strings],
            [QRegExp(r"[*+-*/]"), magenta]
        ]

        # self.highlightingRules.append((QRegExp("([\\\"'])((?:\\1|.)*?)\\1"), strings))
        self.highlightingRules.append((QRegExp("\".*\""), strings))
        self.highlightingRules.append((QRegExp("\'.*\'"), strings))

    def highlight_comments(self, text: str):
        multi_line_comment_format = QTextCharFormat()
        multi_line_comment_format.setForeground(QColor("#88846f"))

        start_expression = r'/*'
        end_expression = r'*/'

        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = index_of(text, start_expression)

        while start_index >= 0:
            end_index = index_of(text, end_expression, start_index)
            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + len(end_expression)

            self.setFormat(start_index, comment_length, multi_line_comment_format)
            start_index = index_of(text, start_expression, start_index + comment_length)

    # VIRTUAL FUNCTION WE OVERRIDE THAT DOES ALL THE COLLORING
    def highlightBlock(self, text):
        # for every pattern
        for pattern, frmat in self.highlightingRules:
            # Create a regular expression from the retrieved pattern
            expression = QRegExp(pattern)
            # Check what index that expression occurs at with the ENTIRE text
            index = expression.indexIn(text)
            # While the index is greater than 0
            while index >= 0:
                # Get the length of how long the expression is true, set the frmat from the start to the length with the text frmat
                length = expression.matchedLength()
                self.setFormat(index, length, frmat)
                # Set index to where the expression ends in the text
                index = expression.indexIn(text, index + length)

        self.highlight_comments(text)

    def update_highlighter(self, val):
        resalt_format = QTextCharFormat()
        resalt_format.setFontItalic(True)
        resalt_format.setBackground(QColor("#d9d779"))
        self.highlightingRules.append((QRegExp(val), resalt_format))


class QCodeEditor(QPlainTextEdit):
    class NumberBar(QWidget):
        def __init__(self, editor):
            QWidget.__init__(self, editor)

            self.editor = editor
            self.editor.blockCountChanged.connect(self.updateWidth)
            self.editor.updateRequest.connect(self.updateContents)
            self.font = QFont()
            self.numberBarColor = QColor("#e8e8e8")

        def paintEvent(self, event):

            painter = QPainter(self)
            painter.fillRect(event.rect(), self.numberBarColor)

            block = self.editor.firstVisibleBlock()

            # Iterate over all visible text blocks in the document.
            while block.isValid():
                blockNumber = block.blockNumber()
                block_top = (
                    self.editor.blockBoundingGeometry(block)
                        .translated(self.editor.contentOffset())
                        .top()
                )

                # Check if the position of the block is out side of the visible area.
                if not block.isVisible() or block_top >= event.rect().bottom():
                    break

                # We want the line number for the selected line to be bold.
                if blockNumber == self.editor.textCursor().blockNumber():
                    self.font.setBold(True)
                    painter.setPen(QColor("#000000"))
                else:
                    self.font.setBold(False)
                    painter.setPen(QColor("#717171"))
                painter.setFont(self.font)

                # Draw the line number right justified at the position of the line.
                paint_rect = QRect(
                    0, block_top, self.width(), self.editor.fontMetrics().height()
                )
                painter.drawText(paint_rect, Qt.AlignRight, str(blockNumber + 1))

                block = block.next()

            painter.end()

            QWidget.paintEvent(self, event)

        def getWidth(self):
            count = self.editor.blockCount()
            width = self.fontMetrics().width(str(count)) + 10
            return width

        def updateWidth(self):
            width = self.getWidth()
            if self.width() != width:
                self.setFixedWidth(width)
                self.editor.setViewportMargins(width, 0, 0, 0)

        def updateContents(self, rect, scroll):
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update(0, rect.y(), self.width(), rect.height())

            if rect.contains(self.editor.viewport().rect()):
                fontSize = self.editor.currentCharFormat().font().pointSize()
                self.font.setPointSize(fontSize)
                self.font.setStyle(QFont.StyleNormal)
                self.updateWidth()

    def __init__(
            self,
            parent,
            DISPLAY_LINE_NUMBERS=True,
            HIGHLIGHT_CURRENT_LINE=True,
            SyntaxHighlighter=XMLHighlighter,
            filename="",
            path="",
            *args
    ):
        """
        Parameters
        ----------
        DISPLAY_LINE_NUMBERS : bool 
            switch on/off the presence of the lines number bar
        HIGHLIGHT_CURRENT_LINE : bool
            switch on/off the current line highliting
        SyntaxHighlighter : QSyntaxHighlighter
            should be inherited from QSyntaxHighlighter
        
        """
        super(QCodeEditor, self).__init__(parent)
        self.filename = filename
        self.path = path

        self.setFont(QFont("Ubuntu Mono", 11))
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.DISPLAY_LINE_NUMBERS = DISPLAY_LINE_NUMBERS

        if DISPLAY_LINE_NUMBERS:
            self.number_bar = self.NumberBar(self)

        if HIGHLIGHT_CURRENT_LINE:
            self.currentLineNumber = None
            self.currentLineColor = self.palette().alternateBase()
            self.currentLineColor = QColor("#3e3d33")
            self.cursorPositionChanged.connect(self.highligtCurrentLine)

        if SyntaxHighlighter is not None:  # add highlighter to textdocument
            self.highlighter = SyntaxHighlighter(self.document())

    def resizeEvent(self, *e):
        """overload resizeEvent handler"""

        if self.DISPLAY_LINE_NUMBERS:  # resize number_bar widget
            cr = self.contentsRect()
            rec = QRect(cr.left(), cr.top(), self.number_bar.getWidth(), cr.height())
            self.number_bar.setGeometry(rec)

        QPlainTextEdit.resizeEvent(self, *e)

    def highligtCurrentLine(self):
        newCurrentLineNumber = self.textCursor().blockNumber()
        if newCurrentLineNumber != self.currentLineNumber:
            self.currentLineNumber = newCurrentLineNumber
            hi_selection = QTextEdit.ExtraSelection()
            hi_selection.format.setBackground(self.currentLineColor)
            hi_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection()
            self.setExtraSelections([hi_selection])
