import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Visibility Toggle Example")

        # Initialize the widget whose visibility is being tracked
        self.tracked_widget = QLabel("I'm visible!")
        self.tracked_widget.visibilityChanged.connect(self.toggle_button_enabled)

        # Initialize the QPushButton
        self.toggle_button = QPushButton("Toggle Visibility")
        self.toggle_button.setEnabled(False)  # Initially disabled

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.tracked_widget)
        layout.addWidget(self.toggle_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def toggle_button_enabled(self, isVisible):
        # Enable or disable the QPushButton based on the visibility of the tracked widget
        self.toggle_button.setEnabled(isVisible)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
