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


class EditView(QMainWindow):

    text_edited = pyqtSignal(str)
    file_opened = pyqtSignal(str)
    has_text_selection_changed = pyqtSignal(bool)
    open_file_requested = pyqtSignal()
    open_recent_file_requested = pyqtSignal(str)
    new_file_requested = pyqtSignal()
    save_file_requested = pyqtSignal()
    save_file_as_requested = pyqtSignal()
    toggle_copilot_field_requested = pyqtSignal(bool)

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MVC Editor")

        self.plainTextEdit = QPlainTextEdit()
        self.plainTextEdit.textChanged.connect(self.on_text_changed)
        self.plainTextEdit.selectionChanged.connect(self.on_text_selection_changed)
        layout = QVBoxLayout()

        layout.addWidget(self.plainTextEdit)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.createMenus()

    def createMenus(self):
        menuBar = self.menuBar()
        self.fileMenu = menuBar.addMenu("&File")  # type: ignore

        self.newAction = self.fileMenu.addAction("&New")  # type: ignore
        self.newAction.setShortcut("Ctrl+N")  # type: ignore
        self.newAction.triggered.connect(self.new_file_requested.emit)  # type: ignore
        self.fileMenu.addAction(self.newAction)  # type: ignore

        self.openAction = self.fileMenu.addAction("&Open")  # type: ignore
        self.openAction.setShortcut("Ctrl+O")  # type: ignore
        self.openAction.triggered.connect(self.open_file_requested.emit)  # type: ignore
        self.fileMenu.addAction(self.openAction)  # type: ignore

        self.saveAction = self.fileMenu.addAction("&Save")  # type: ignore
        self.saveAction.setShortcut("Ctrl+S")  # type: ignore
        self.saveAction.triggered.connect(self.save_file_requested.emit)  # type: ignore
        self.fileMenu.addAction(self.saveAction)  # type: ignore

        self.saveAsAction = self.fileMenu.addAction("&Save As")  # type: ignore
        self.saveAsAction.setShortcut("Ctrl+Shift+S")  # type: ignore
        self.saveAsAction.triggered.connect(self.save_file_as_requested.emit)  # type: ignore
        self.fileMenu.addAction(self.saveAsAction)  # type: ignore

        self.fileMenu.addSeparator()  # type: ignore

        self.recentFilesMenu = self.fileMenu.addMenu("&Recent Files")  # type: ignore

        self.fileMenu.addSeparator()  # type: ignore

        self.exitAction = self.fileMenu.addAction("&Exit")  # type: ignore
        self.exitAction.setShortcut("Ctrl+Q")  # type: ignore
        self.exitAction.triggered.connect(self.close)  # type: ignore
        self.fileMenu.addAction(self.exitAction)  # type: ignore

        self.editMenu = self.menuBar().addMenu("&Edit")  # type: ignore

        self.copyAction = self.editMenu.addAction("&Copy")  # type: ignore
        self.copyAction.setShortcut("Ctrl+C")  # type: ignore
        self.copyAction.triggered.connect(self.plainTextEdit.copy)  # type: ignore
        self.editMenu.addAction(self.copyAction)  # type: ignore

        self.cutAction = self.editMenu.addAction("&Cut")  # type: ignore
        self.cutAction.setShortcut("Ctrl+X")  # type: ignore
        self.cutAction.triggered.connect(self.plainTextEdit.cut)  # type: ignore
        self.editMenu.addAction(self.cutAction)  # type: ignore

        self.pasteAction = self.editMenu.addAction("&Paste")  # type: ignore
        self.pasteAction.setShortcut("Ctrl+V")  # type: ignore
        self.pasteAction.triggered.connect(self.plainTextEdit.paste)  # type: ignore
        self.editMenu.addAction(self.pasteAction)  # type: ignore

        self.viewMenu = self.menuBar().addMenu("&View")  # type: ignore

        self.showCopilotAction = self.viewMenu.addAction("&Show Copilot field")  # type: ignore
        self.showCopilotAction.setCheckable(True)  # type: ignore
        self.showCopilotAction.setChecked(True)  # type: ignore
        self.showCopilotAction.toggled.connect(self.on_toggle_copilot_field_requested)  # type: ignore
        self.viewMenu.addAction(self.showCopilotAction)  # type: ignore

    def update_data(self, data):
        if self.plainTextEdit.toPlainText() != data:
            self.plainTextEdit.setPlainText(data)

    def on_toggle_copilot_field_requested(self):
        self.toggle_copilot_field_requested.emit(self.showCopilotAction.isChecked())

    def on_text_changed(self):
        self.text_edited.emit(self.plainTextEdit.toPlainText())

    def on_text_selection_changed(self):
        self.has_text_selection_changed.emit(self.plainTextEdit.textCursor().hasSelection())

    def set_save_enabled(self, enabled):
        self.saveAction.setEnabled(enabled)  # type: ignore

    def set_save_as_enabled(self, enabled):
        self.saveAsAction.setEnabled(enabled)  # type: ignore

    def set_cut_enabled(self, enabled):
        self.cutAction.setEnabled(enabled)  # type: ignore

    def set_copy_enabled(self, enabled):
        self.copyAction.setEnabled(enabled)  # type: ignore

    def update_recent_files(self, recent_files):
        self.recentFilesMenu.clear()  # type: ignore
        for file_name in recent_files:
            action = self.recentFilesMenu.addAction(file_name)  # type: ignore
            action.triggered.connect(lambda bool, file_name=file_name: self.open_recent_file_requested.emit(file_name))  # type: ignore
        pass

    def showErrorMessage(self, title, message):
        QMessageBox.warning(self, title, message)
