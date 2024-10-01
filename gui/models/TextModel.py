from PyQt5.QtCore import QObject, pyqtSignal


class TextModel(QObject):
    data_changed = pyqtSignal(str)
    modified_data_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._data = ""
        self._is_modified = False

    def set_data(self, data):
        if self._data != data:
            self._data = data
            self.data_changed.emit(data)
            self.set_modified(True)

    def get_data(self):
        return self._data

    def set_modified(self, is_modified):
        if self._is_modified != is_modified:
            self._is_modified = is_modified
            self.modified_data_changed.emit(is_modified)

    def is_modified(self):
        return self._is_modified
