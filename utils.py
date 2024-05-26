from PySide6.QtWidgets import QScrollArea
def set_scroll(scroll_area:QScrollArea):
    return scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().maximum())


