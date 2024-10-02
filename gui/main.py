import sys

sys.path.append("/home/carl/dev/Notepad.AI/")

from gui.controllers.MainController import *
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    controller = MainController()
    controller.run()
    app.exec_()
