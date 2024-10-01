from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt


class LineEditView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window flags to remove title bar and make it a tool window
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)

        # Create layout
        layout = QVBoxLayout()

        # Create line edit
        self.lineEdit = QLineEdit()

        # Add line edit to layout
        layout.addWidget(self.lineEdit)

        # Set layout margins to 0 to make it compact
        layout.setContentsMargins(0, 0, 0, 0)

        # Set the layout for the widget
        self.setLayout(layout)

        # Set a fixed size for the widget (adjust as needed)
        self.setFixedSize(200, 30)

        # Optional: Set stylesheet for a border (comment out if not needed)
        self.setStyleSheet("border: 1px solid gray;")

    def getText(self):
        return self.lineEdit.text()

    def clearText(self):
        self.lineEdit.setText("")
