import json
import os
import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit
)
from qfluentwidgets import Dialog

from PySide6.QtGui import QIcon , QColor
from qfluentwidgets.components.widgets import SingleDirectionScrollArea , ToolButton , LineEdit
from qfluentwidgets import (FluentIcon as FIF)
from PySide6.QtCore import Qt
from responses import Process_Models
from Editor import Editor , text_boxes , refresh_text_boxes
from icon import SearchLineEdit
class Main_Widget(QWidget):
    """
    A class representing the Free GPT application window.
    """
    def __init__(self):
        """
        Initialize the Free GPT application window.
        """
        super().__init__()
        self.setObjectName("Main_Widget")

        # Main Layout Setup
        self.main_layout = QGridLayout()
        self.main_layout.setColumnStretch(0, 0)
        self.main_layout.setColumnStretch(1, 1)
        self.setLayout(self.main_layout)

        # Sidebar Setup
        # side_bar_frame = QFrame()
        # side_bar_frame.setFrameStyle(QFrame.Shape.Panel)
        # self.main_layout.addWidget(side_bar_frame, 0, 0)

        # side_bar_layout = QVBoxLayout()
        # side_bar_frame.setLayout(side_bar_layout)

        # Chat Bar Setup
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setSpacing(10)
        self.main_layout.addLayout(self.chat_layout, 0, 1)

        # chat_frame = QFrame()
        # chat_frame.setFrameShape(QFrame.Shape.StyledPanel)
        # self.chat_layout.addWidget(chat_frame)

        container_widget = QWidget()
        self.chats_grid_layout = QGridLayout()
        self.scroll_area = SingleDirectionScrollArea()
        self.scroll_area.setStyleSheet("background-color: transparent;")
        container_widget.setLayout(self.chats_grid_layout)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(container_widget)
        self.chat_layout.addWidget(self.scroll_area)

        # Prompt Bar Setup
        prompt_layout = QHBoxLayout()
        self.chat_layout.addLayout(prompt_layout)
        self.prompt_entry = SearchLineEdit()
        self.prompt_entry.setFixedHeight(50)
        self.prompt_entry.setPlaceholderText("Enter prompt here")
        self.prompt_entry.setStyleSheet("""
    QLineEdit {
        color: rgb(0, 0, 0);
        background-color: rgb(255, 255, 255);
        border: 1px solid rgb(0, 0, 0);
        border-radius: 25px;
        padding-left: 20px;
    }                                
        """)
        prompt_layout.addWidget(self.prompt_entry)

        self.send_button = ToolButton(FIF.SEND_FILL , "")
        self.send_button.clicked.connect(self.Create_text_box)
        prompt_layout.addWidget(self.send_button)

        # Load responses
        self.load_responses()


    def Create_text_box(self):
        """
        Create a text box for the prompt and a response text box, and add them to the chat grid layout.
        Also process the prompt and response using the Process_Models function.
        """
        
        # Get the text from the prompt entry and clear it
        prompt_text = self.prompt_entry.text()
        if prompt_text == "":
            return
        self.prompt_entry.clear()

        # Display the prompt text in the chat grid layout
        self.display_message(prompt_text, alignment=Qt.AlignmentFlag.AlignLeft)

        # Create an Editor widget for the response
        res_text_box = Editor(True)   
        
        # Add the response text box to the chat grid layout
        self.chats_grid_layout.addWidget(res_text_box,  # Response text box
                                         len(text_boxes),  # Row index
                                         0,  # Column index
                                         alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)  # Alignment

        # Process the prompt
        Process_Models(prompt_text,
                       res_text_box, 
                       self.send_button, 
                       self.prompt_entry,
                       self.scroll_area) 

    def load_responses(self):
        """
        Load the chat history from chat_history.json and display it in the chat grid layout.
        """
        history_file = 'chat_history.json'
        if os.path.exists(history_file):
            with open(history_file) as file:
                data = json.load(file)
            for item in data:
                prompt_text = item["prompt"]
                response_text = item["response"]
                self.display_message(prompt_text, Qt.AlignmentFlag.AlignLeft)
                self.display_message(response_text, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

    def display_message(self, text, alignment):
        """
        Create and display a message in the chat grid layout.
        """
        text_box = Editor()
        text_box.Load_text(text)
        self.chats_grid_layout.addWidget(text_box, len(text_boxes), 0 , alignment=alignment)
        text_box.auto_resize(text_box.get_current_text_edit())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_Widget()
    window.show()
    refresh_text_boxes()
    sys.exit(app.exec())
