from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from gui.views.LineEditView import LineEditView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MVC Editor")
        self.setCentralWidget(QWidget())
        self.central_layout = QVBoxLayout(self.centralWidget())

        self.createMenus()

    def createMenus(self):
        menuBar = self.menuBar()
        self.fileMenu = menuBar.addMenu("&File")  # type: ignore

        self.newAction = self.fileMenu.addAction("&New")  # type: ignore
        self.newAction.setShortcut("Ctrl+N")  # type: ignore
        self.fileMenu.addAction(self.newAction)  # type: ignore

        self.openAction = self.fileMenu.addAction("&Open")  # type: ignore
        self.openAction.setShortcut("Ctrl+O")  # type: ignore
        self.fileMenu.addAction(self.openAction)  # type: ignore

        self.saveAction = self.fileMenu.addAction("&Save")  # type: ignore
        self.saveAction.setShortcut("Ctrl+S")  # type: ignore
        self.fileMenu.addAction(self.saveAction)  # type: ignore

        self.saveAsAction = self.fileMenu.addAction("&Save As")  # type: ignore
        self.saveAsAction.setShortcut("Ctrl+Shift+S")  # type: ignore
        self.fileMenu.addAction(self.saveAsAction)  # type: ignore

        self.fileMenu.addSeparator()  # type: ignore

        self.recentFilesMenu = self.fileMenu.addMenu("&Recent Files")  # type: ignore

        self.fileMenu.addSeparator()  # type: ignore

        self.exitAction = self.fileMenu.addAction("&Exit")  # type: ignore
        self.exitAction.setShortcut("Ctrl+Q")  # type: ignore
        self.fileMenu.addAction(self.exitAction)  # type: ignore

        self.editMenu = self.menuBar().addMenu("&Edit")  # type: ignore

        self.copyAction = self.editMenu.addAction("&Copy")  # type: ignore
        self.copyAction.setShortcut("Ctrl+C")  # type: ignore
        self.editMenu.addAction(self.copyAction)  # type: ignore

        self.cutAction = self.editMenu.addAction("&Cut")  # type: ignore
        self.cutAction.setShortcut("Ctrl+X")  # type: ignore
        self.editMenu.addAction(self.cutAction)  # type: ignore

        self.pasteAction = self.editMenu.addAction("&Paste")  # type: ignore
        self.pasteAction.setShortcut("Ctrl+V")  # type: ignore
        self.editMenu.addAction(self.pasteAction)  # type: ignore

        self.editMenu.addSeparator()  # type: ignore

        self.findAction = self.editMenu.addAction("&Find...")  # type: ignore
        self.findAction.setShortcut("Ctrl+F")  # type: ignore
        self.editMenu.addAction(self.findAction)  # type: ignore

        self.replaceAction = self.editMenu.addAction("&Replace...")  # type: ignore
        self.replaceAction.setShortcut("Ctrl+H")  # type: ignore
        self.editMenu.addAction(self.replaceAction)  # type: ignore

        self.viewMenu = self.menuBar().addMenu("&View")  # type: ignore

        self.showCopilotAction = self.viewMenu.addAction("&Show Copilot field")  # type: ignore
        self.showCopilotAction.setCheckable(True)  # type: ignore
        self.showCopilotAction.setChecked(True)  # type: ignore
        self.viewMenu.addAction(self.showCopilotAction)  # type: ignore

    def close(self):
        super().close()
        if QApplication.instance().quitOnLastWindowClosed():
            QApplication.instance().quit()
