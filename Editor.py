import re
from turtle import width
from qfluentwidgets.components.widgets import PushButton , LineEdit , TextEdit ,CardWidget
from PySide6.QtWidgets import QWidget , QVBoxLayout , QTextEdit , QLabel
from pyHighlight import PythonHighlighter
from PySide6.QtCore import Qt , QSize
from PySide6.QtGui import QFontMetrics , QTextOption


Editor_Style = """
QTextEdit{
    padding: 2px;
    color: rgb(0, 0, 0);
    background-color: rgb(255, 255, 255);
    border: 1px solid rgb(0, 0, 0);
    border-radius: 10px;
}
"""
text_boxes = []

class Editor(QWidget):

    def __init__(self,streaming=False):
        """
        Initialize the Editor class.

        Args:
            streaming (bool, optional): Whether the editor is in streaming mode.
                                        Defaults to False.
        """
        # Call the parent class constructor
        super().__init__()
        self.setObjectName("Editor")

        # Initialize instance variables
        self.text_edits = []  # List to store text_edit widgets
        self.total_text = ""  # String to store total text
        self.is_code = False  # Boolean to indicate if the text is code
        self.text_layout = QVBoxLayout(self)  # Layout for text_edit widgets
        text_boxes.append(self)  # Add this editor to the list of text_boxes
        self.setStyleSheet(Editor_Style)  # Set the style sheet
        self.streaming = streaming  # Set the streaming mode
        
        # Add a text_edit widget if streaming mode is enabled
        if self.streaming:
            self.add_text_box()

        # Set the layout and show the widget
        self.setLayout(self.text_layout)
        
    def auto_resize(self, text_edit: QTextEdit):
        """
        Automatically resize the QTextEdit widget to fit its content.

        Args:
            text_edit (QTextEdit): The QTextEdit widget to be resized.
        """
        text_edit.show()
        height = int(text_edit.document().size().height() +
                        text_edit.contentsMargins().top() +
                        text_edit.contentsMargins().bottom())

        # # Set the height of the text_edit widget to the calculated height.
        text_edit.setFixedHeight(height)

    def Load_text(self, text: str | list):
        """
        Load text into the editor.

        Args:
            text (str | list): The text to load into the editor.
                               If a list is provided, it will be joined into a string.
        """
        if isinstance(text, list):
            # If the text is a list, join it into a string
            text = "".join([str(t) for t in text if t])

            # Find code and text segments in the text
            segments = self.find_code_and_text_segments(text)

            # Add a text box for each segment and set its text
            for segment in segments:
                self.add_text_box(segment[1])
                text = self.fix_text(segment[0])
                self.text_edit.insertPlainText(text)
        else:
            # If the text is not a list, add a text box and set its text
            self.add_text_box()
            text = self.fix_text(text)
            self.text_edit.insertPlainText(text)
    
    def Stream_text(self, text: str):
        """
        Append the incoming text to the total text and check if it contains a code block.
        If the text contains a code block, add a text box for the code block.
        Otherwise, add a text box for the text.
        Insert the incoming text into the current text box.

        Args:
            text (str): The text to be streamed.
        """
        # Append the incoming text to the total text
        self.total_text += text

        # Check if the text contains a code block
        if self.check_text():
            # If the text is code, add a text box for the code
            if not self.is_code:
                self.add_text_box(True)
        else:
            # If the text is not code, add a text box for the text
            if self.is_code:
                self.add_text_box()

        # Fix the text by removing unnecessary characters
        text = self.fix_text(text)

        # Move the text cursor to the end of the current text box
        cursor = self.text_edit.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)

        # Insert the incoming text into the current text box
        self.text_edit.insertPlainText(text)

    def get_current_text_edit(self) -> QTextEdit:
        """
        Returns the current QTextEdit widget.

        Returns:
            QTextEdit: The current text edit widget.
        """
        # Returns the QTextEdit widget that is currently being used
        # to display the text.
        return self.text_edit

    def add_text_box(self, is_code=False):
        """
        Adds a new QTextEdit widget to the layout.

        Args:
            is_code (bool, optional): Whether the text edit widget is for code.
                                      Defaults to False.
        """
        # Create a new QTextEdit widget
        self.text_edit = QTextEdit()
        # Set the frame shape and shadow
        self.text_edit.setFrameShape(QTextEdit.Shape.Panel)
        self.text_edit.setFrameShadow(QTextEdit.Shadow.Plain)
        
        # Set the text edit as read-only
        self.text_edit.setReadOnly(True)
        
        # Set the fixed width of the text edit
        self.text_edit.setFixedWidth(600)
        self.text_edit.setFixedHeight(30)
        # Add the text edit to the list of text edits
        self.text_edits.append(self.text_edit)
        
        # Add the text edit to the layout
        self.text_layout.addWidget(self.text_edit)
        
        # Set the is_code flag
        self.is_code = is_code
        
        # Connect the textChanged signal to the auto_resize function
        self.text_edit.textChanged.connect(
            lambda: self.auto_resize(self.get_current_text_edit()))
        
        # If the text edit is for code, set the highlighter
        if self.is_code:
            self.text_edit.highlighter = PythonHighlighter(
                self.text_edit.document())

    def check_text(self):
        """
        Check if the total text contains an odd number of triple backticks.

        Returns:
            bool: True if the total text contains an odd number of triple backticks, False otherwise.
        """
        # Count the number of triple backticks in the total text.
        # If the count is odd, it indicates that a code block is currently open.
        # Otherwise, it is completely closed.
        return True if self.total_text.count("```") % 2 == 1 else False
    
    def fix_text(self, Text: str):
        """
        Remove any instances of backticks and double newlines from the given text.

        Args:
            Text (str): The text to be fixed.

        Returns:
            str: The fixed text.
        """
        # Remove any instances of backticks
        if "`" in Text:
            Text = Text.replace("`", "")
        # Remove any double newlines
        if "\n\n" in Text:
            Text = Text.replace("\n\n", "")
        return Text
    
    def find_code_and_text_segments(self , Text):
        """
        Returns a list of tuples, each containing a segment of the text, a boolean
        indicating whether it is a code block, and the language name if it is a code block.

        Parameters:
        text (str): The string containing potential code blocks.

        Returns:
        list: A list of tuples with each containing a segment of text, a boolean,
            and the language name (str or None).
        """
        # Regular expression pattern to find code blocks with any language
        pattern = r"```(\w+)?\s(.*?)```"
        # Find all matches and their positions
        matches = list(re.finditer(pattern, Text, flags=re.DOTALL))
        last_idx = 0
        segments = []

        for match in matches:
            # Get text before the code block
            start, end = match.span()
            non_code = Text[last_idx:start]
            if non_code:
                segments.append((non_code, False, None))
            
            # Get the code block
            lang = match.group(1) or "plaintext"  # Default to plaintext if no language is specified
            code = match.group(2)
            segments.append((code, True, lang))
            
            last_idx = end
        
        # Get any remaining text after the last code block
        if last_idx < len(Text):
            segments.append((Text[last_idx:], False, None))
        
        return segments

def refresh_text_boxes():
        """
        Refresh the text boxes in the chat grid layout.
        """
        for text_box in text_boxes:
            for text in text_box.text_edits:
                text_box.auto_resize(text)