from PyQt5.QtCore import QObject, pyqtSignal
from gui.views.LineEditView import LineEditView


class LineEditController(QObject):
    text_executed = pyqtSignal(str)

    def __init__(self, main_view, line_edit_view):
        super().__init__()

        self._line_edit_view = line_edit_view
        self._main_view = main_view
        self._connect_signals()

    def _connect_signals(self):
        self._line_edit_view.lineEdit.returnPressed.connect(self.on_return_pressed)

    def on_return_pressed(self):
        text = self._line_edit_view.getText()
        self.text_executed.emit(text)

    def setVisible(self, state):
        self._line_edit_view.setVisible(state)

    def clearText(self):
        self._line_edit_view.clearText()
