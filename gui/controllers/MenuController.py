from PyQt5.QtCore import QObject, pyqtSignal
from gui.views.EditView import *
from gui.models.FileNameModel import FileNameModel
from gui.models.TextModel import TextModel


class MenuController(QObject):
    new_file_requested = pyqtSignal()
    open_file_requested = pyqtSignal()
    save_file_requested = pyqtSignal()
    save_file_as_requested = pyqtSignal()
    open_recent_file_requested = pyqtSignal(str)
    exit_requested = pyqtSignal()

    copy_requested = pyqtSignal()
    cut_requested = pyqtSignal()
    paste_requested = pyqtSignal()
    find_requested = pyqtSignal()
    replace_requested = pyqtSignal()

    toggle_copilot_field_requested = pyqtSignal(bool)

    def __init__(self, main_window, edit_view, file_name_model, text_model, recent_files_model):
        super().__init__()

        self._main_window = main_window
        self._edit_view = edit_view
        self._file_name_model = file_name_model
        self._text_model = text_model
        self._recent_files_model = recent_files_model

        self._text_model.modified_data_changed.connect(self.on_modified_data_changed)
        self._edit_view.has_text_selection_changed.connect(self.on_has_text_selection_changed)
        self._recent_files_model.recent_files_changed.connect(self.update_recent_files)

        self._connect_actions()

    def _connect_actions(self):

        self._main_window.newAction.triggered.connect(self.new_file_requested.emit)  # type: ignore
        self._main_window.openAction.triggered.connect(self.open_file_requested.emit)  # type: ignore
        self._main_window.saveAction.triggered.connect(self.save_file_requested.emit)  # type: ignore
        self._main_window.saveAsAction.triggered.connect(self.save_file_as_requested.emit)  # type: ignore
        self._main_window.exitAction.triggered.connect(self.exit_requested.emit)  # type: ignore
        self._main_window.copyAction.triggered.connect(self.copy_requested.emit)  # type: ignore
        self._main_window.cutAction.triggered.connect(self.cut_requested.emit)  # type: ignore
        self._main_window.pasteAction.triggered.connect(self.paste_requested.emit)  # type: ignore
        self._main_window.findAction.triggered.connect(self.find_requested.emit)  # type: ignore
        self._main_window.replaceAction.triggered.connect(self.replace_requested.emit)  # type: ignore
        self._main_window.showCopilotAction.toggled.connect(self.on_toggle_copilot_field_requested)  # type: ignore

    def on_modified_data_changed(self, is_modified):
        self.set_save_enabled(is_modified)
        self.set_save_as_enabled(is_modified)

    def on_has_text_selection_changed(self, has_selection):
        self.set_cut_enabled(has_selection)
        self.set_copy_enabled(has_selection)

    def update_recent_files(self, recent_files):
        self.update_recent_files(recent_files)

    def on_toggle_copilot_field_requested(self):
        self.toggle_copilot_field_requested.emit(self.showCopilotAction.isChecked())

    def set_save_enabled(self, enabled):
        self._main_window.saveAction.setEnabled(enabled)  # type: ignore

    def set_save_as_enabled(self, enabled):
        self._main_window.saveAsAction.setEnabled(enabled)  # type: ignore

    def set_cut_enabled(self, enabled):
        self._main_window.cutAction.setEnabled(enabled)  # type: ignore

    def set_copy_enabled(self, enabled):
        self._main_window.copyAction.setEnabled(enabled)  # type: ignore

    def update_recent_files(self, recent_files):
        self._main_window.recentFilesMenu.clear()  # type: ignore
        for file_name in recent_files:
            action = self._main_window.recentFilesMenu.addAction(file_name)  # type: ignore
            action.triggered.connect(lambda bool, file_name=file_name: self.open_recent_file_requested.emit(file_name))  # type: ignore
