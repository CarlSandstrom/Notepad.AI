from PyQt5.QtCore import QObject, pyqtSignal
from gui.views.EditView import *
from gui.models.FileNameModel import FileNameModel
from gui.models.TextModel import TextModel


class MenuController(QObject):
    def __init__(self, view, file_name_model, text_model, recent_files_model):
        super().__init__()

        self._view = view
        self._file_name_model = file_name_model
        self._text_model = text_model
        self._recent_files_model = recent_files_model

        self._text_model.modified_data_changed.connect(self.on_modified_data_changed)
        self._view.has_text_selection_changed.connect(self.on_has_text_selection_changed)
        self._recent_files_model.recent_files_changed.connect(self.update_recent_files)

    def on_modified_data_changed(self, is_modified):
        self._view.set_save_enabled(is_modified)
        self._view.set_save_as_enabled(is_modified)

    def on_has_text_selection_changed(self, has_selection):
        self._view.set_cut_enabled(has_selection)
        self._view.set_copy_enabled(has_selection)

    def update_recent_files(self, recent_files):
        self._view.update_recent_files(recent_files)
