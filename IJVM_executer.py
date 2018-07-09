import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from graphics.UIs.ui import Ui_MainWindow
import time
import threading
from Memory import Memory
from datapath.CPP import CPP
from datapath.PC import PC
from datapath.LV import LV
from datapath.SP import SP
from CU.CUdesign import CU


def memory_initialization():
    instructions = open("codes/assembled/instructions.txt", "r").read().split()
    constants = open("codes/assembled/constants.txt", "r").read().split()
    local_vars = open("codes/assembled/local_vars.txt", "r").read().split()
    instructions = list(map(lambda q: int(q, 16), instructions))
    constants = list(map(lambda q: int(q, 16), constants))
    local_vars = list(map(lambda q: int(q, 16), local_vars))
    Memory.data[PC.data:PC.data+len(instructions)] = instructions
    Memory.data[LV.data:LV.data+len(local_vars)] = local_vars
    Memory.data[CPP.data:CPP.data+len(constants)] = constants
    SP.data = LV.data + len(local_vars)


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

    # as an example:
    def abc(self):
        time.sleep(2)
        ex.ui.mar_ld_start(100)
        time.sleep(2)
        ex.ui.signals_stop()


if __name__ == '__main__':
    memory_initialization()
    app = QApplication(sys.argv)
    ex = App()
    CU.ui = ex

    # as an example:
    threading.Thread(target=ex.abc).start()

    print(123)
    sys.exit(app.exec_())


