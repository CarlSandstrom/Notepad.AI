from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)

from gui.views.LineEditView import LineEditView


class EditView(QWidget):

    text_edited = pyqtSignal(str)
    has_text_selection_changed = pyqtSignal(bool)

    def __init__(self) -> None:
        super().__init__()

        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.textChanged.connect(self.on_text_changed)
        self.plainTextEdit.selectionChanged.connect(self.on_text_selection_changed)
        layout = QVBoxLayout()

        layout.addWidget(self.plainTextEdit)
        self.setLayout(layout)

    def update_data(self, data):
        if self.plainTextEdit.toPlainText() != data:
            self.plainTextEdit.setPlainText(data)

    def showErrorMessage(self, title, message):
        QMessageBox.warning(self, title, message)

    def on_text_changed(self):
        self.text_edited.emit(self.plainTextEdit.toPlainText())

    def on_text_selection_changed(self):
        self.has_text_selection_changed.emit(self.plainTextEdit.textCursor().hasSelection())
