from typing import List, Union
from PySide6.QtCore import QSize, Qt, QRectF, Signal, QPoint, QTimer, QEvent, QAbstractItemModel, Property
from PySide6.QtGui import QPainter, QPainterPath, QIcon, QCursor, QAction
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QToolButton, QTextEdit,
                               QPlainTextEdit, QCompleter, QStyle, QWidget , QPushButton)

from qfluentwidgets.common import FluentStyleSheet, themeColor , Icon , FluentIconBase
from qfluentwidgets import FluentIcon as FIF 
from qfluentwidgets.components.widgets import SingleDirectionScrollArea , ToolButton , LineEdit
from qfluentwidgets import ProgressRing , IndeterminateProgressRing

class SearchLineEdit(LineEdit):
    """ Search line edit """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.spin= LineEditButton(FIF.SEARCH, self)
        self.hBoxLayout.addWidget(self.spin, 0, Qt.AlignRight)
        self.setTextMargins(0, 0, 59, 0)
        self.spin.setVisible(False)

# class SearchLineEdit(QLineEdit):
#     """ Search line edit """
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         # self.searchButton = LineEditButton(FIF.SEARCH, self)
#         self.hBoxLayout = QHBoxLayout(self)
#         # self.hBoxLayout.addWidget(self.searchButton, 0, Qt.AlignRight)
#         box = IndeterminateProgressRing(self)
#         box.setVisible(False)
#         self.hBoxLayout.addWidget(box, 0, Qt.AlignRight)
#         self.setTextMargins(0, 0, 59, 0)

class LineEditButton(IndeterminateProgressRing):
    """ Line edit button """

    def __init__(self, icon: Union[str, QIcon], parent=None):
        super().__init__(parent=parent)
        self._icon = icon
        self.isPressed = False
        self.setFixedSize(31, 23)
        # self.setIconSize(QSize(10, 10))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName('lineEditButton')
        FluentStyleSheet.LINE_EDIT.apply(self)

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        iw, ih = self.size().width(), self.size().height()
        w, h = self.width(), self.height()
        rect = QRectF((w - iw)/2, (h - ih)/2, iw, ih)

        if self.isPressed:
            painter.setOpacity(0.7)


