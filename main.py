import sys
from PySide6 import QtWidgets
from qfluentwidgets import (
    FluentWindow,
    NavigationItemPosition,
    FluentIcon as FIF,
     
)

from qfluentwidgets.common.icon import toQIcon
from Editor import refresh_text_boxes
from main_widget import Main_Widget
from settings import Widget
import ctypes
myappid = 'g4f.myproduct.subproduct.1.0' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)



class Main_Window(FluentWindow):
    """Constructor for the main window of the Free GPT application.
    
    Arguments:
        app (QApplication): The Qt application object
    """
    def __init__(self):
        super(Main_Window, self).__init__()
        self.setWindowTitle("G4F")
        self._main_widget = Main_Widget()
        self.setWindowIcon(toQIcon(FIF.APPLICATION))
        self.addSubInterface(self._main_widget,FIF.HOME,  "Main", NavigationItemPosition.SCROLL)
        self.addSubInterface(Widget('Settings', self), FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # qdarktheme.setup_theme("light")
    window = Main_Window()
    window.show()
    refresh_text_boxes()
    sys.exit(app.exec())