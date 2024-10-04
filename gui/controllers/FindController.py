from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QTextDocument

from gui.views.FindView import FindView


class FindController(QObject):
    def __init__(self, menu_controller, text_model, text_view):
        super().__init__()

        self._menu_controller = menu_controller
        self._text_model = text_model
        self._text_view = text_view

        self.dialog = FindView(self._menu_controller._main_window)

        self._connect_signals()

        self._last_position = 0
        self._last_direction = None
        self._last_match_start = None
        self._last_match_end = None

    def _connect_signals(self):
        self._menu_controller.find_requested.connect(self.on_find)
        self.dialog.find_next_requested.connect(self.on_find_next)
        self.dialog.find_previous_requested.connect(self.on_find_previous)

    def on_find(self):
        self.dialog.show()

    def on_find_next(self, search_text, case_sensitive):
        self._find(search_text, case_sensitive)

    def on_find_previous(self, search_text, case_sensitive):
        self._find(search_text, case_sensitive, forward=False)

    def _find(self, search_text, case_sensitive, forward=True):
        if not search_text:
            return

        text = self._text_model.get_data()

        if not case_sensitive:
            text = text.lower()
            search_text = search_text.lower()

        # Adjust starting position when changing direction
        if self._last_direction is not None and self._last_direction != forward:
            if forward:
                # Switching from previous to next
                self._last_position = self._last_match_end if self._last_match_end is not None else 0
            else:
                # Switching from next to previous
                self._last_position = self._last_match_start if self._last_match_start is not None else len(text)

        if forward:
            start_pos = text.find(search_text, self._last_position)
            if start_pos == -1:  # If not found, wrap around to the beginning
                start_pos = text.find(search_text, 0)
        else:
            # For backward search, we need to search from the beginning up to the last position
            start_pos = text.rfind(search_text, 0, self._last_position)
            if start_pos == -1:  # If not found, wrap around to the end
                start_pos = text.rfind(search_text)

        if start_pos != -1:
            end_pos = start_pos + len(search_text)
            self._last_match_start = start_pos
            self._last_match_end = end_pos
            self._last_position = end_pos if forward else start_pos
            self._text_view.set_selection(start_pos, end_pos)
            self._last_direction = forward
        else:
            # Handle case when text is not found
            print(f"Text '{search_text}' not found.")
            self._last_match_start = None
            self._last_match_end = None
