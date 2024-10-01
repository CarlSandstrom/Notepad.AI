from EditMainController import *
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    controller = EditMainController()
    controller.run()
    app.exec_()
