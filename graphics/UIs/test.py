import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from graphics.UIs.ui import Ui_MainWindow
import time
import threading


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

    def abc(self):
        time.sleep(2)
        ex.ui.mar_ld_start(100)
        time.sleep(2)
        ex.ui.signals_stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    threading.Thread(target=ex.abc).start()
    print(123)
    sys.exit(app.exec_())
