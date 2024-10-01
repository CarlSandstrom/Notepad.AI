import json
import os
from PyQt5.QtCore import QObject, pyqtSignal
from appdirs import user_data_dir

class RecentFilesModel(QObject):
    recent_files_changed = pyqtSignal(list)

    def __init__(self, max_recent_files=10, app_name="MVCEditor"):
        super().__init__()
        self._recent_files = []
        self._max_recent_files = max_recent_files
        self._app_name = app_name
        self._data_dir = user_data_dir(self._app_name, appauthor=False)
        self._recent_files_path = os.path.join(self._data_dir, "recent_files.json")
        self.load_recent_files()

    def add_recent_file(self, file_path):
        if file_path in self._recent_files:
            self._recent_files.remove(file_path)
        self._recent_files.insert(0, file_path)
        if len(self._recent_files) > self._max_recent_files:
            self._recent_files.pop()
        self._save_recent_files()
        self.recent_files_changed.emit(self._recent_files)

    def get_recent_files(self):
        return self._recent_files

    def remove_recent_file(self, file_path):
        if file_path in self._recent_files:
            self._recent_files.remove(file_path)
            self._save_recent_files()
            self.recent_files_changed.emit(self._recent_files)

    def clear_recent_files(self):
        self._recent_files.clear()
        self._save_recent_files()
        self.recent_files_changed.emit(self._recent_files)

    def load_recent_files(self):
        if os.path.exists(self._recent_files_path):
            try:
                with open(self._recent_files_path, 'r') as f:
                    self._recent_files = json.load(f)
                self._recent_files = self._recent_files[:self._max_recent_files]
            except json.JSONDecodeError:
                self._recent_files = []
        else:
            self._recent_files = []
        self.recent_files_changed.emit(self._recent_files)

    def _save_recent_files(self):
        os.makedirs(self._data_dir, exist_ok=True)
        with open(self._recent_files_path, 'w') as f:
            json.dump(self._recent_files, f)