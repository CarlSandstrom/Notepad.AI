from PyQt5.QtCore import QObject, pyqtSignal


class FileNameModel(QObject):
    file_name_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._filename = ""

    def set_file_name(self, filename):
        if self._filename != filename:
            self._filename = filename
            self.file_name_changed.emit(filename)

    def get_file_name(self):
        return self._filename
