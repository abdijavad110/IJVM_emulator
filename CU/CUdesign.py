from Main import memory
from datapath.ALU import ALU
from datapath.H import H
from datapath.LV import LV
from datapath.MAR import MAR
from datapath.MDR import MDR
from datapath.OPC import OPC
from datapath.PC import PC
from datapath.MBR import MBR
from datapath.SP import SP
from datapath.TOS import TOS


def fetch():
    # enable pc  and MBR ld and rd of memory and increment of ALU
    ALU.controller = "110101"
    ALU.b_update(PC.data)

    # sys pause

    MBR.load(memory[PC])
    PC.load(ALU.out)


def wr():
    memory[MAR] = MDR.data


def bipush(T):
    # sp on bus to alu and enable sp ld
    ALU.controller = "110101"
    ALU.b_update(SP.data)

    # sys

    SP.load(ALU.out)
    MAR.load(ALU.out)
    fetch()
    # sys
    # b should be out of alu

    ALU.controller = "010100"
    ALU.b_update(MBR.data)
    # sys
    MDR.load(ALU.out)
    TOS.load(ALU.out)
    wr()



def GOTO(T):
    # ld of opc should be enabled and pc is on alu bus
    ALU.controller = "110110"
    ALU.b_update(PC.data)

    # sys
    OPC.load(ALU.out)
    fetch()
    ALU.controller = "011111"
    ALU.b_update(MBR.data)

    # sys

    H.load(ALU.out)

def LADD(T):
    ALU.controller = "010100"
    ALU.b_update(LV.data)

    # sys
    H.load(ALU.out)

def IFEQ(T):
    pass


def IFLT(T):
    pass


def IF_ICMPEQ(T):
    pass


def IINC(T):
    pass


def ILOAD(T):
    pass


def ISTORE(T):
    pass


def ISUB(T):
    pass


def NOPE(T):
    pass


class CU:



    def clocked(T):


        if (T==0):
             fetch()
        else:
                      N={0x10: bipush(T),
                       0xA7: GOTO(T),
                       0x60: LADD(T),
                       0x99: IFEQ(T),
                       0x9B: IFLT(T),
                       0x9F: IF_ICMPEQ(T),
                       0x84: IINC(T),
                       0x15: ILOAD(T),
                       0x36: ISTORE(T),
                       0x64: ISUB(T),
                       0x00: NOPE(T),
                       }[MBR.data]

