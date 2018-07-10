import threading

from codes.assembler import assemble
from Memory import Memory
from datapath.PC import PC
from datapath.SP import SP
from datapath.CPP import CPP
from datapath.LV import LV
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


def new_btn_clicked():
    print("1")
    pass


def open_btn_clicked():
    asm = open("codes/deafult_input_assembly.txt", "r")
    asm_r = asm.read()
    asm.close()
    return asm_r


def save_btn_clicked(value):
    asm = open("codes/deafult_input_assembly.txt", "w")
    asm.write(value)
    asm.close()


def save_as_btn_clicked():
    print("4")
    pass


def assemble_btn_clicked():
    assemble()
    memory_initialization()
    print(Memory.data)
    threading.Thread(target=CU.clocked).start()


def run_btn_clicked():
    print("6")
    pass


def step_fwd_btn_clicked():
    CU.flag = False
    pass


def clear_btn_clicked():
    pass
