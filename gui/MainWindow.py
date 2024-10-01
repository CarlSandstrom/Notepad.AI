import sys

sys.path.append("/home/carl/dev/Notepad.AI/")

from gui.controllers.EditMainController import *
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    controller = EditMainController()
    controller.run()
    app.exec_()
