from PySide6 import QtWidgets , QtCore
from qfluentwidgets import SubtitleLabel, setFont



class Widget(QtWidgets.QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QtWidgets.QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, QtCore.Qt.AlignCenter)

        # Must set a globally unique object name for the sub-interface
        self.setObjectName(text.replace(' ', '-'))