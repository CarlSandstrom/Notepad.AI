from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox
from PyQt5.QtCore import pyqtSignal


class FindView(QDialog):
    find_next_requested = pyqtSignal(str, bool)
    find_previous_requested = pyqtSignal(str, bool)

    close_requested = pyqtSignal()

    def __init__(self, parent=None):
        super(FindView, self).__init__(parent)

        self.setWindowTitle("Find")
        self.setModal(False)

        layout = QVBoxLayout()

        find_layout = QHBoxLayout()
        find_layout.addWidget(QLabel("Find:"))

        self._find_text = QLineEdit()
        find_layout.addWidget(self._find_text)
        layout.addLayout(find_layout)

        self.case_sensitive = QCheckBox("Case sensitive")
        layout.addWidget(self.case_sensitive)

        button_layout = QHBoxLayout()

        find_next_button = QPushButton("Find next")
        find_next_button.clicked.connect(self.on_find_next)
        button_layout.addWidget(find_next_button)

        find_previous_button = QPushButton("Find previous")
        find_previous_button.clicked.connect(self.on_find_previous)
        button_layout.addWidget(find_previous_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close_requested.emit)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def find_text(self):
        return self._find_text

    def case_sensitive(self):
        return self.case_sensitive

    def on_find_next(self):
        self.find_next_requested.emit(self._find_text.text(), self.case_sensitive.isChecked())

    def on_find_previous(self):
        self.find_previous_requested.emit(self._find_text.text(), self.case_sensitive.isChecked())
