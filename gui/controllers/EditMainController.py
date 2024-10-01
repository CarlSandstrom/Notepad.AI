from typing import Any
from EditView import *
from FileController import *
from FileNameModel import *
from MenuController import *
from TextModel import *
from WindowTitleController import *
from RecentFilesModel import *


class EditMainController(QObject):
    def __init__(self):
        super().__init__()
        self._text_model = TextModel()
        self._file_name_model = FileNameModel()

        self._view = EditView()

        self._window_title_controller = WindowTitleController(
            self._view, self._file_name_model, self._text_model
        )

        self._recent_files_model = RecentFilesModel(max_recent_files=10)

        self._menu_controller = MenuController(
            self._view, self._file_name_model, self._text_model, self._recent_files_model
        )
        
        self._file_controller = FileController(
            self._view, self._file_name_model, self._text_model
        )


        self._connect_signals()

        self._initialize_state()

    def run(self):
        self._view.show()

    def set_data(self, data):
        self._text_model.set_data(data)

    def on_file_opened(self, file_name):
        if not os.path.isfile(file_name):
            self._view.showErrorMessage ( "File not found", f"{file_name} does not exist.")
            self._recent_files_model.remove_recent_file(file_name)
            return
        self._file_name_model.set_file_name(file_name)
        self._text_model.set_data(open(file_name).read())
        self._text_model.set_modified(False)

    def on_recent_file_opened(self, file_name):
        self.on_file_opened(file_name)

    def _connect_signals(self):
        self._view.text_edited.connect(self._text_model.set_data)

        self._text_model.data_changed.connect(self._view.update_data)
        self._file_controller.file_saved.connect(self.on_file_saved)
        self._file_controller.file_opened.connect(self.on_file_opened)
        self._recent_files_model.recent_files_changed.connect(
            self._menu_controller.update_recent_files
        )
        self._view.open_recent_file_requested.connect(
            self.on_recent_file_opened
        )

        self._view.file_opened.connect(self.on_file_opened)

    def _initialize_state(self):
        self._text_model.set_data("")
        self._file_name_model.set_file_name("Untitled")
        self._text_model.set_modified(False)
        self._window_title_controller.update_window_title()
        self._menu_controller.on_modified_data_changed(False)
        self._menu_controller.on_has_text_selection_changed(False)
        self._recent_files_model.load_recent_files()
        
    def on_file_saved(self, file_name):
        self._recent_files_model.add_recent_file(file_name)
    