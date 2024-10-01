from PyQt5.QtCore import QObject, pyqtSignal
from gui.views.LineEditView import LineEditView


class LineEditController(QObject):
    text_executed = pyqtSignal(str)

    def __init__(self, main_view):
        super().__init__()

        self._view = LineEditView()
        self._main_view = main_view
        self._connect_signals()

    def _connect_signals(self):
        self._view.lineEdit.returnPressed.connect(self.on_return_pressed)

    def on_return_pressed(self):
        text = self._view.getText()
        self.text_executed.emit(text)

    def setVisible(self, state):
        self._view.setVisible(state)
