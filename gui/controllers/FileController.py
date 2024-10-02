from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog


class FileController(QObject):
    file_opened = pyqtSignal(str)
    file_saved = pyqtSignal(str)

    def __init__(self, view, file_name_model, text_model):
        super().__init__()

        self._view = view
        self._file_name_model = file_name_model
        self._text_model = text_model

        self._view.openAction.triggered.connect(self.open_file)
        self._view.saveAction.triggered.connect(self.save_file)
        self._view.saveAsAction.triggered.connect(self.save_file_as)
        self._view.newAction.triggered.connect(self.new_file)

    def open_file(self):
        file_dialog = QFileDialog(self._view)
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Text files (*.txt);; All files (*.*)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            with open(file_path, "r") as f:
                content = f.read()
            self._text_model.set_data(content)
            self._file_name_model.set_file_name(file_path)
            self._text_model.set_modified(False)
            self.file_opened.emit(file_path)

    def save_file(self):
        if self._file_name_model.get_file_name() == "Untitled":
            self.save_file_as()
        else:
            self._save_current_file()

    def save_file_as(self, filename=None):
        file_dialog = QFileDialog(self._view)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        # Show text files or all files
        file_dialog.setNameFilter("Text files (*.txt);;All files (*.*)")
        if filename is not None:
            file_dialog.selectFile(filename)

        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self._file_name_model.set_file_name(file_path)
            self._save_current_file()

    def new_file(self):
        self._text_model.set_data("")
        self._file_name_model.set_file_name("Untitled")
        self._text_model.set_modified(False)

    def _save_current_file(self):
        file_path = self._file_name_model.get_file_name()
        with open(file_path, "w") as f:
            f.write(self._text_model.get_data())
        self._text_model.set_modified(False)
        self.file_saved.emit(file_path)
