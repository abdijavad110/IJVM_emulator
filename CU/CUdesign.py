from Memory import Memory
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




class CU:
    T=0


    def clocked(self):
        if T == 0:
            fetch()
        else:
            N = {0x10: bipush(T),
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

def fetch():
    # enable pc  and MBR ld and rd of memory and increment of ALU
    ALU.controller = "110101"
    ALU.b_update(PC.data)

    # sys pause

    MBR.load(Memory.read(PC.data))
    PC.load(ALU.out)
    T +=1

def rd():
     MDR.load(Memory.read(MAR.data))

def wr():
    Memory.word_write(MDR.data, MAR.data)

def bipush():
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

def GOTO(self):
    # ld of opc should be enabled and pc is on alu bus
    ALU.controller = "110110"
    ALU.b_update(PC.data)

    # sys
    OPC.load(ALU.out)
    fetch()
    #     ld of H should be enabled
    ALU.controller = "011111"
    ALU.b_update(MBR.data)
    fetch()
    # sys

    H.load(ALU.out)
    ALU.controller = "011100"
    ALU.b_update(MBRU.data)
    ALU.a_update(H.data)
    #     ld of H should be enabled
    # sys
    H.load(ALU.out)
    ALU.controller = "111100"
    ALU.b_update(OPC.data)
    ALU.a_update(H.data)
    #     sys
    PC.load(ALU.out)


def LADD(self):
    # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
    ALU.controller = "110110"
    ALU.b_update(SP.data)
#     sys
    MAR.load(ALU.out)
    SP.load(ALU.out)
#     enable ld of H ,tos is on bus
    ALU.controller = "010100"
    ALU.b_update(TOS.data)
#   sys

    H.load(ALU.out)
    # enable ld of tos and MDR
    ALU.controller = "111100"
    ALU.b_update(MDR.data)
    ALU.a_update(H.data)
#   sys
    MDR.load(ALU.out)
    TOS.load(ALU.out)
    wr()






def IFEQ(self):
    # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
    ALU.controller = "110110"
    ALU.b_update(SP.data)
    #     sys
    MAR.load(ALU.out)
    SP.load(ALU.out)
    # rd of memory is enabled

    rd()
#     enable ld of opc...tos is on bus

    ALU.controller = "010100"
    ALU.b_update(TOS.data)

#   sys
    OPC.load(ALU.out)
#   enable ld of tos and MDR is on bus
    ALU.controller = "010100"
    ALU.b_update(MDR.data)
# sys
    TOS.load(ALU.out)
#     opc is on bus to check if it is zero
    ALU.controller = "010100"
    ALU.b_update(OPC.data)

    if ALU.Z:
        # enable ld OPC
        ALU.controller = "110110"
        ALU.b_update(PC.data)
         #     sys
        OPC.load(ALU.out)
        GOTO()

    else:
        # ld pc enable to be incremented
        ALU.controller = "110101"
        ALU.b_update(PC.data)

        # sys pause
        PC.load(ALU.out)

        # ld pc enable to be incremented
        ALU.controller = "110101"
        ALU.b_update(PC.data)

        # sys pause
        PC.load(ALU.out)



def IFLT(self):
    # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
    ALU.controller = "110110"
    ALU.b_update(SP.data)
    #     sys
    MAR.load(ALU.out)
    SP.load(ALU.out)
    # rd of memory is enabled
    rd()
    #     enable ld of opc...tos is on bus

    ALU.controller = "010100"
    ALU.b_update(TOS.data)

    #   sys
    OPC.load(ALU.out)
    #   enable ld of tos and MDR is on bus
    ALU.controller = "010100"
    ALU.b_update(MDR.data)
    # sys
    TOS.load(ALU.out)
    #     opc is on bus to check if it is zero
    ALU.controller = "010100"
    ALU.b_update(OPC.data)

    if ALU.N:
        # enable ld OPC
        ALU.controller = "110110"
        ALU.b_update(PC.data)
        #     sys
        OPC.load(ALU.out)
        GOTO()

    else:
        # ld pc enable to be incremented
        ALU.controller = "110101"
        ALU.b_update(PC.data)

        # sys pause
        PC.load(ALU.out)

        # ld pc enable to be incremented
        ALU.controller = "110101"
        ALU.b_update(PC.data)

        # sys pause
        PC.load(ALU.out)


def IF_ICMPEQ():
    # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
    ALU.controller = "110110"
    ALU.b_update(SP.data)
    #     sys
    MAR.load(ALU.out)
    SP.load(ALU.out)
    # rd of memory is enabled
    rd()
    # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
    ALU.controller = "110110"
    ALU.b_update(SP.data)
    #     sys
    MAR.load(ALU.out)
    SP.load(ALU.out)
#     mdr is on bus and ld of H is enabled and rd of memory is enabled
    ALU.controller = "010100"
    ALU.b_update(H.data)
#     sys
    H.load(ALU.out)
    # rd of memory is enabled
    rd()
    #     enable ld of opc...tos is on bus

    ALU.controller = "010100"
    ALU.b_update(TOS.data)

    #   sys
    OPC.load(ALU.out)
    #   enable ld of tos and MDR is on bus
    ALU.controller = "010100"
    ALU.b_update(MDR.data)
    # sys
    TOS.load(ALU.out)
#     opc is on bus and alu is wants to have opc - H in the out
    ALU.controller = "111111"
    ALU.b_update(OPC.data)
    ALU.a_update(H.data)
    if ALU.Z:
        # enable ld OPC
        ALU.controller = "110110"
        ALU.b_update(PC.data)
         #     sys
        OPC.load(ALU.out)
        GOTO()

    else:
        # ld pc enable to be incremented
        ALU.controller = "110101"
        ALU.b_update(PC.data)

        # sys pause
        PC.load(ALU.out)

        # ld pc enable to be incremented
        ALU.controller = "110101"
        ALU.b_update(PC.data)

        # sys pause
        PC.load(ALU.out)



def IINC():


    # در نظر گرفته که ابتدا varnumبیاد بعد const...هر دو رو هم یک بایتی در نظر گرفته
    fetch()
#     enable ld of H and LV is on bus
    ALU.controller = "010100"
    ALU.b_update(LV.data)
#     sys
    H.load(ALU.out)
#     enable ld of MAR and MBRU is on bus
    ALU.controller = "111100"
    ALU.b_update(MBR.data)
    ALU.a_update(H.data)
#     sys
    MAR.load(ALU.out)
    rd()
    fetch()
    #     enable ld of H and MDR is on bus
    ALU.controller = "010100"
    ALU.b_update(MDR.data)
    #     sys
    H.load(ALU.out)

#     enable ld of MDR and MBR is on bus
    ALU.controller = "111100"
    ALU.b_update(MBR.data)
    ALU.a_update(H.data)
# sys
    MDR.load(ALU.out)
    wr()



def ILOAD(self):
    # در نظر گرفته که ابتدا varnumبیاد بعد const...هر دو رو هم یک بایتی در نظر گرفته
    fetch()
    #     enable ld of H and LV is on bus
    ALU.controller = "010100"
    ALU.b_update(LV.data)
    #     sys
    H.load(ALU.out)
    #     enable ld of MAR and MBRU is on bus
    ALU.controller = "111100"
    ALU.b_update(MBR.data)
    ALU.a_update(H.data)
    #     sys
    MAR.load(ALU.out)
    # ed of memory
    rd()

    # ld of sp and MAR should be enabled and sp is on alu bus
    ALU.controller = "110101"
    ALU.b_update(SP.data)
    #     sys
    MAR.load(ALU.out)
    SP.load(ALU.out)
#     wr of memory
    wr()
#     enable ld of TOS and MDR is on bus
    ALU.controller = "010100"
    ALU.b_update(MDR.data)
    #     sys
    TOS.load(ALU.out)


def ISTORE(self):
    # در نظر گرفته که ابتدا varnumبیاد بعد const...هر دو رو هم یک بایتی در نظر گرفته
    fetch()
    #     enable ld of H and LV is on bus
    ALU.controller = "010100"
    ALU.b_update(LV.data)
    #     sys
    H.load(ALU.out)
    #     enable ld of MAR and MBRU is on bus
    ALU.controller = "111100"
    ALU.b_update(MBR.data)
    ALU.a_update(H.data)
    #     sys
    MAR.load(ALU.out)
    #     enable ld of MDR and Tos is on bus
    ALU.controller = "010100"
    ALU.b_update(TOS.data)
    #     sys
    MDR.load(ALU.out)
    wr()

    # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
    ALU.controller = "110110"
    ALU.b_update(SP.data)
    #     sys
    MAR.load(ALU.out)
    SP.load(ALU.out)
    #     rd of memory
    rd()


    #     enable ld of TOS and MDR is on bus
    ALU.controller = "010100"
    ALU.b_update(MDR.data)
    #     sys
    TOS.load(ALU.out)


def ISUB():
    # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
    ALU.controller = "110110"
    ALU.b_update(SP.data)
    #     sys
    MAR.load(ALU.out)
    SP.load(ALU.out)
#     rd of memory
    rd()

    #     enable ld of H ,tos is on bus
    ALU.controller = "010100"
    ALU.b_update(TOS.data)
    #   sys

    H.load(ALU.out)
    # enable ld of tos and MDR
    ALU.controller = "111111"
    ALU.b_update(MDR.data)
    ALU.a_update(H.data)
    #   sys
    MDR.load(ALU.out)
    TOS.load(ALU.out)
    wr()

def NOPE():
    pass