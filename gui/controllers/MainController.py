from typing import Any
from gui.services.AIService import AIService
from gui.views.EditView import *
from gui.views.MainWindow import *
from gui.models.FileNameModel import *
from gui.models.TextModel import *
from gui.models.RecentFilesModel import *
from gui.controllers.MenuController import *
from gui.controllers.FileController import *
from gui.controllers.WindowTitleController import *
from gui.controllers.LineEditController import *


class MainController(QObject):
    def __init__(self):
        super().__init__()

        self._init_models()
        self._init_views()
        self._init_controllers()
        self._init_services()

        self._connect_signals()
        self._initialize_state()

    def _init_models(self):
        self._text_model = TextModel()
        self._file_name_model = FileNameModel()
        self._recent_files_model = RecentFilesModel(max_recent_files=10)

    def _init_views(self):
        self._main_window = MainWindow()
        self._edit_view = EditView()
        self._line_edit_view = LineEditView()

        self._main_window.central_layout.addWidget(self._edit_view)

    def _init_controllers(self):
        self._window_title_controller = WindowTitleController(
            self._main_window, self._file_name_model, self._text_model
        )
        self._menu_controller = MenuController(
            self._main_window, self._edit_view, self._file_name_model, self._text_model, self._recent_files_model
        )
        self._file_controller = FileController(self._main_window, self._file_name_model, self._text_model)
        self._line_edit_controller = LineEditController(self._main_window, self._line_edit_view)

    def _init_services(self):
        self._ai_service = AIService()

    def run(self):
        self._main_window.show()

    def set_data(self, data):
        self._text_model.set_data(data)

    def on_file_opened(self, file_name):
        if not os.path.isfile(file_name):
            self._edit_view.showErrorMessage("File not found", f"{file_name} does not exist.")
            self._recent_files_model.remove_recent_file(file_name)
            return
        self._file_name_model.set_file_name(file_name)
        self._text_model.set_data(open(file_name).read())
        self._text_model.set_modified(False)

    def on_recent_file_opened(self, file_name):
        self.on_file_opened(file_name)

    def _connect_signals(self):
        self._edit_view.text_edited.connect(self._text_model.set_data)

        self._text_model.data_changed.connect(self._edit_view.update_data)
        self._file_controller.file_saved.connect(self.on_file_saved)
        self._file_controller.file_opened.connect(self.on_file_opened)
        self._recent_files_model.recent_files_changed.connect(self._menu_controller.update_recent_files)
        self._menu_controller.exit_requested.connect(self.on_exit)

        self._menu_controller.open_recent_file_requested.connect(self.on_recent_file_opened)
        self._menu_controller.toggle_copilot_field_requested.connect(self.on_toggle_copilot_field)

        self._line_edit_controller.text_executed.connect(self.on_line_edit_executed)

    def _initialize_state(self):
        self._text_model.set_data("")
        self._file_name_model.set_file_name("Untitled")
        self._text_model.set_modified(False)
        self._window_title_controller.update_window_title()
        self._menu_controller.on_modified_data_changed(False)
        self._menu_controller.on_has_text_selection_changed(False)
        self._recent_files_model.load_recent_files()
        self._line_edit_controller.setVisible(True)

    def on_file_saved(self, file_name):
        self._recent_files_model.add_recent_file(file_name)

    def on_toggle_copilot_field(self, state):
        self._line_edit_controller.setVisible(state)

    def on_exit(self):
        self._main_window.close()

    def on_line_edit_executed(self, text):
        self._line_edit_controller.clearText()

        print(text)

        predicted_intent, slot_contents = self._ai_service.process_text(text)
        pass
