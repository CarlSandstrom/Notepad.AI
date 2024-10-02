from gui.views.EditView import *
from gui.models.TextModel import *


class WindowTitleController(QObject):
    def __init__(self, main_window, file_name_model, text_model):
        super().__init__()
        self._main_window = main_window
        self._file_name_model = file_name_model
        self._text_model = text_model

        self._file_name = ""
        self._is_modified = False

        self._file_name_model.file_name_changed.connect(self.set_file_name)
        self._text_model.modified_data_changed.connect(self.set_modified)

    def update_window_title(self):
        file_name = self._file_name
        is_modified = self._is_modified
        title = f"{file_name}{' - *' if is_modified else ''}"
        self._main_window.setWindowTitle(title)

    def set_file_name(self, file_name):
        self._file_name = file_name
        self.update_window_title()

    def set_modified(self, is_modified):
        self._is_modified = is_modified
        self.update_window_title()
