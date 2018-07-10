import time

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
import threading


# from graphics.UIs.ui import Ui_MainWindow


class CU:
    T = 0
    ui = None
    flag = False
    curter = threading.Thread

    @staticmethod
    def clocked():
        while True:
            print("clocked,   flag: " + str(CU.flag) + "    T: " + str(CU.T))
            CU.flag = True
            while CU.flag:
                continue
            CU.fetch()
            if CU.T == 0:
                CU.fetch()
            elif CU.T == 1:
                print(hex(MBR.data)[-2:])
                if hex(MBR.data)[-2:] == "10":
                    CU.bipush()
                elif hex(MBR.data)[-2:] == "a7":
                    CU.GOTO()
                elif hex(MBR.data)[-2:] == "60":
                    CU.LADD()
                elif hex(MBR.data)[-2:] == "99":
                    CU.IFEQ()
                elif hex(MBR.data)[-2:] == "9b":
                    CU.IFLT()
                elif hex(MBR.data)[-2:] == "9f":
                    CU.IF_ICMPEQ()
                elif hex(MBR.data)[-2:] == "84":
                    CU.IINC()
                elif hex(MBR.data)[-2:] == "15":
                    CU.ILOAD()
                elif hex(MBR.data)[-2:] == "36":
                    CU.ISTORE()
                elif hex(MBR.data)[-2:] == "64":
                    CU.ISUB()
                elif hex(MBR.data)[-2:] == "00":
                    CU.NOPE()
                elif hex(MBR.data)[-2:] == "0":
                    CU.NOPE()
                else:
                    print("undefined opcode")

    @staticmethod
    def fetch():
        if CU.T == 0:
            CU.T += 1
        print("fetching")
        ALU.controller = "110101"
        ALU.b_update(PC.data)

        # sys pause
        CU.ui.signals_stop()
        CU.ui.mbr_ld_start()
        CU.ui.pc_ld_start()
        CU.flag = True
        while CU.flag:
            time.sleep(1)
        #
        CU.ui.mbr_ld_update(Memory.read(PC.data))
        CU.ui.pc_ld_update(ALU.out)

        MBR.load(Memory.read(PC.data))
        PC.load(ALU.out)

    @staticmethod
    def rd():
        print("reading")
        #
        CU.ui.mdr_ld_start()
        CU.ui.mdr_ld_update(Memory.read(MAR.data))
        #
        MDR.load(Memory.read(MAR.data))

    @staticmethod
    def wr():
        print("writing")
        Memory.word_write(MDR.data, MAR.data)

    @staticmethod
    def bipush():
        print("bipush")
        CU.T += 1
        # sp on bus to alu and enable sp ld

        ALU.controller = "110101"
        ALU.b_update(SP.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.sp_out_start()
        CU.ui.sp__ld_start()
        CU.ui.mar_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.sp__ld_update(ALU.out)
        CU.ui.mar_ld_update(ALU.out)
        SP.load(ALU.out)
        MAR.load(ALU.out)
        CU.fetch()
        # sys
        # b should be out of alu

        ALU.controller = "010100"
        ALU.b_update(MBR.data)
        # sys
        CU.ui.signals_stop()
        CU.ui.mdr_ld_start()
        CU.ui.tos_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mdr_ld_update(ALU.out)
        CU.ui.tos_ld_update(ALU.out)
        MDR.load(ALU.out % 256)
        TOS.load(ALU.out % 256)
        CU.wr()
        CU.ui.stack_add(ALU.out % 256)
        CU.T = 0

    @staticmethod
    def GOTO():
        print("goto")
        CU.T += 1
        # ld of opc should be enabled and pc is on alu bus
        ALU.controller = "110110"
        ALU.b_update(PC.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.opc_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.opc_ld_update(ALU.out)

        OPC.load(ALU.out)
        CU.fetch()
        #     ld of H should be enabled
        ALU.controller = "011111"
        ALU.b_update(MBR.data)
        CU.fetch()

        # sys
        CU.ui.signals_stop()
        CU.ui.h_ld_start()
        CU.ui.mbr_out1_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.h_ld_update(ALU.out)
        H.load(ALU.out)
        ALU.controller = "011100"
        ALU.b_update(MBR.data)
        ALU.a_update(H.data)
        #     ld of H should be enabled

        # sys
        CU.ui.signals_stop()
        CU.ui.h_ld_start()
        CU.ui.mbr_out2_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.h_ld_update(ALU.out)
        H.load(ALU.out)
        ALU.controller = "111100"
        ALU.b_update(OPC.data)
        ALU.a_update(H.data)

        #     sys
        CU.ui.signals_stop()
        CU.ui.pc_ld_start()
        CU.ui.opc_out_start()

        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.pc_ld_update(ALU.out)
        PC.load(ALU.out)
        CU.T = 0

    @staticmethod
    def LADD():
        print("iadd")
        CU.T += 1
        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        #     sys
        CU.ui.signals_stop()
        CU.ui.mar_ld_start()
        CU.ui.sp__ld_start()
        CU.ui.sp_out_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mar_ld_update(ALU.out)
        CU.ui.sp__ld_update(ALU.out)

        MAR.load(ALU.out)
        SP.load(ALU.out)
        #     enable ld of H ,tos is on bus
        ALU.controller = "010100"
        ALU.b_update(TOS.data)

        #   sys
        CU.ui.signals_stop()
        CU.ui.tos_out_start()
        CU.ui.h_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.h_ld_update(ALU.out)
        H.load(ALU.out)
        # enable ld of tos and MDR
        ALU.controller = "111100"
        ALU.b_update(MDR.data)
        ALU.a_update(H.data)

        #   sys
        CU.ui.signals_stop()
        CU.ui.mdr_out_start()
        CU.ui.tos_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.tos_ld_update(ALU.out)
        MDR.load(ALU.out)
        TOS.load(ALU.out)
        CU.wr()
        CU.T = 0

    @staticmethod
    def IFEQ():
        print("ifeq")
        CU.T += 1
        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        #     sys
        CU.ui.signals_stop()
        CU.ui.sp_out_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mar_ld_update(ALU.out)
        CU.ui.sp__ld_update(ALU.out)
        MAR.load(ALU.out)
        SP.load(ALU.out)
        # rd of memory is enabled

        CU.rd()
        #     enable ld of opc...tos is on bus

        ALU.controller = "010100"
        ALU.b_update(TOS.data)

        #   sys
        CU.ui.signals_stop()
        CU.ui.tos_out_start()
        CU.ui.opc_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.opc_ld_update(ALU.out)
        OPC.load(ALU.out)
        #   enable ld of tos and MDR is on bus
        ALU.controller = "010100"
        ALU.b_update(MDR.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.mdr_out_start()
        CU.ui.tos_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.tos_ld_update(ALU.out)
        TOS.load(ALU.out)
        #     opc is on bus to check if it is zero
        ALU.controller = "010100"
        ALU.b_update(OPC.data)

        #     sys
        CU.ui.signals_stop()
        CU.ui.opc_out_start()
        CU.flag = True
        while CU.flag:
            continue
        #

        if ALU.Z:
            # enable ld OPC
            ALU.controller = "110110"
            ALU.b_update(PC.data)

            #     sys
            CU.ui.signals_stop()
            CU.ui.pc_out_start()
            CU.ui.opc_ld_start()
            CU.flag = True
            while CU.flag:
                continue
            #
            CU.ui.opc_ld_update(ALU.out)
            OPC.load(ALU.out)
            CU.GOTO()

        else:
            # ld pc enable to be incremented
            ALU.controller = "110101"
            ALU.b_update(PC.data)

            # sys pause
            CU.ui.signals_stop()
            CU.ui.pc_out_start()
            CU.ui.pc_ld_start()
            CU.flag = True
            while CU.flag:
                continue
            #
            CU.ui.pc_ld_update(ALU.out)
            PC.load(ALU.out)

            # ld pc enable to be incremented
            ALU.controller = "110101"
            ALU.b_update(PC.data)

            # sys pause
            CU.ui.signals_stop()
            CU.ui.pc_out_start()
            CU.ui.pc_ld_start()
            CU.flag = True
            while CU.flag:
                continue
            #
            CU.ui.pc_ld_update(ALU.out)

            PC.load(ALU.out)
            CU.T = 0

    @staticmethod
    def IFLT():
        print("iflt")
        CU.T += 1
        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.sp_out_start()
        CU.ui.mar_ld_start()
        CU.ui.sp__ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mar_ld_update(ALU.out)
        CU.ui.sp__ld_update(ALU.out)
        MAR.load(ALU.out)
        SP.load(ALU.out)
        # rd of memory is enabled
        CU.rd()
        #     enable ld of opc...tos is on bus

        ALU.controller = "010100"
        ALU.b_update(TOS.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.tos_out_start()
        CU.ui.opc_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.opc_ld_update(ALU.out)
        OPC.load(ALU.out)
        #   enable ld of tos and MDR is on bus
        ALU.controller = "010100"
        ALU.b_update(MDR.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.mdr_out_start()
        CU.ui.tos_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.tos_ld_update(ALU.out)
        TOS.load(ALU.out)
        #     opc is on bus to check if it is zero
        ALU.controller = "010100"
        ALU.b_update(OPC.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.opc_out_start()
        CU.flag = True
        while CU.flag:
            continue
        #

        if ALU.N:
            # enable ld OPC
            ALU.controller = "110110"
            ALU.b_update(PC.data)

            # sys
            CU.ui.signals_stop()
            CU.ui.pc_out_start()
            CU.ui.opc_ld_start()
            CU.flag = True
            while CU.flag:
                continue
            #
            CU.ui.opc_ld_update(ALU.out)
            OPC.load(ALU.out)
            CU.GOTO()

        else:
            # ld pc enable to be incremented
            ALU.controller = "110101"
            ALU.b_update(PC.data)

            # sys
            CU.ui.signals_stop()
            CU.ui.pc_out_start()
            CU.ui.pc_ld_start()
            CU.flag = True
            while CU.flag:
                continue
            #
            CU.ui.pc_ld_update(ALU.out)
            PC.load(ALU.out)

            # ld pc enable to be incremented
            ALU.controller = "110101"
            ALU.b_update(PC.data)

            # sys
            CU.ui.signals_stop()
            CU.ui.pc_out_start()
            CU.ui.pc_ld_start()
            CU.flag = True
            while CU.flag:
                continue
            #
            CU.ui.pc_ld_update(ALU.out)
            PC.load(ALU.out)
            CU.T = 0

    @staticmethod
    def IF_ICMPEQ():
        print("if_icmpeq")
        CU.T += 1
        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.sp_out_start()
        CU.ui.mar_ld_start()
        CU.ui.sp__ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mar_ld_update(ALU.out)
        CU.ui.sp__ld_update(ALU.out)
        MAR.load(ALU.out)
        SP.load(ALU.out)
        # rd of memory is enabled
        CU.rd()
        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.sp_out_start()
        CU.ui.sp__ld_start()
        CU.ui.mar_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.sp__ld_update(ALU.out)
        CU.ui.mar_ld_update(ALU.out)
        MAR.load(ALU.out)
        SP.load(ALU.out)
        #     mdr is on bus and ld of H is enabled and rd of memory is enabled
        ALU.controller = "010100"
        ALU.b_update(MDR.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.h_ld_start()
        CU.ui.mdr_out_start()

        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.h_ld_update(ALU.out)
        H.load(ALU.out)
        # rd of memory is enabled
        CU.rd()
        #     enable ld of opc...tos is on bus

        ALU.controller = "010100"
        ALU.b_update(TOS.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.tos_out_start()
        CU.ui.opc_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.opc_ld_update(ALU.out)
        OPC.load(ALU.out)
        #   enable ld of tos and MDR is on bus
        ALU.controller = "010100"
        ALU.b_update(MDR.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.mdr_out_start()
        CU.ui.tos_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.tos_ld_update(ALU.out)
        TOS.load(ALU.out)
        #     opc is on bus and alu is wants to have opc - H in the out
        ALU.controller = "111111"
        ALU.b_update(OPC.data)
        ALU.a_update(H.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.opc_out_start()
        CU.flag = True
        while CU.flag:
            continue
        #

        if ALU.Z:
            # enable ld OPC
            ALU.controller = "110110"
            ALU.b_update(PC.data)

            # sys
            CU.ui.signals_stop()
            CU.ui.pc_out_start()
            CU.ui.opc_ld_start()
            CU.flag = True
            while CU.flag:
                continue
            #
            CU.ui.opc_ld_update(ALU.out)
            OPC.load(ALU.out)
            CU.GOTO()

        else:
            # ld pc enable to be incremented
            ALU.controller = "110101"
            ALU.b_update(PC.data)

            # sys
            CU.ui.signals_stop()
            CU.ui.pc_out_start()
            CU.ui.pc_ld_start()
            CU.flag = True
            while CU.flag:
                continue
            #
            CU.ui.pc_ld_update(ALU.out)

            PC.load(ALU.out)

            # ld pc enable to be incremented
            ALU.controller = "110101"
            ALU.b_update(PC.data)

            # sys
            CU.ui.signals_stop()
            CU.ui.pc_out_start()
            CU.ui.pc_ld_start()
            CU.flag = True
            while CU.flag:
                continue
            #
            CU.ui.pc_ld_update(ALU.out)

            PC.load(ALU.out)
            CU.T = 0

    @staticmethod
    def IINC():
        print("iinc")
        CU.T += 1
        # در نظر گرفته که ابتدا varnumبیاد بعد const...هر دو رو هم یک بایتی در نظر گرفته
        CU.fetch()
        #     enable ld of H and LV is on bus
        ALU.controller = "010100"
        ALU.b_update(LV.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.lv_out_start()
        CU.ui.h_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.h_ld_update(ALU.out)
        H.load(ALU.out)
        #     enable ld of MAR and MBRU is on bus
        ALU.controller = "111100"
        ALU.b_update(MBR.data)
        ALU.a_update(H.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.mbr_out2_start()
        CU.ui.mar_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mar_ld_update(ALU.out)
        MAR.load(ALU.out)
        CU.rd()
        CU.fetch()
        #     enable ld of H and MDR is on bus
        ALU.controller = "010100"
        ALU.b_update(MDR.data)
        # sys
        CU.ui.signals_stop()
        CU.ui.mdr_out_start()
        CU.ui.h_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.h_ld_update(ALU.out)
        H.load(ALU.out)

        #     enable ld of MDR and MBR is on bus
        ALU.controller = "111100"
        ALU.b_update(MBR.data)
        ALU.a_update(H.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.mbr_out1_start()
        CU.ui.mdr_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mdr_ld_update(ALU.out)
        MDR.load(ALU.out)
        CU.wr()
        CU.T = 0

    @staticmethod
    def ILOAD():
        print("iload")
        CU.T += 1
        # در نظر گرفته که ابتدا varnumبیاد بعد const...هر دو رو هم یک بایتی در نظر گرفته
        CU.fetch()
        #     enable ld of H and LV is on bus
        ALU.controller = "010100"
        ALU.b_update(LV.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.lv_out_start()
        CU.ui.h_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.h_ld_update(ALU.out)
        H.load(ALU.out)
        #     enable ld of MAR and MBRU is on bus
        ALU.controller = "111100"
        ALU.b_update(MBR.data)
        ALU.a_update(H.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.mbr_out2_start()
        CU.ui.mar_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mar_ld_update(ALU.out)
        MAR.load(ALU.out)
        # ed of memory
        CU.rd()

        # ld of sp and MAR should be enabled and sp is on alu bus
        ALU.controller = "110101"
        ALU.b_update(SP.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.sp_out_start()
        CU.ui.mar_ld_start()
        CU.ui.sp__ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mar_ld_update(ALU.out)
        CU.ui.sp__ld_update(ALU.out)
        MAR.load(ALU.out)
        SP.load(ALU.out)
        #     wr of memory
        CU.wr()
        #     enable ld of TOS and MDR is on bus
        ALU.controller = "010100"
        ALU.b_update(MDR.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.mdr_out_start()
        CU.ui.tos_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.tos_ld_update(ALU.out)
        TOS.load(ALU.out)
        CU.T = 0

    @staticmethod
    def ISTORE():
        print("istore")
        CU.T += 1
        # در نظر گرفته که ابتدا varnumبیاد بعد const...هر دو رو هم یک بایتی در نظر گرفته
        CU.fetch()
        #     enable ld of H and LV is on bus
        ALU.controller = "010100"
        ALU.b_update(LV.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.lv_out_start()
        CU.ui.h_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.h_ld_update(ALU.out)
        H.load(ALU.out)
        #     enable ld of MAR and MBRU is on bus
        ALU.controller = "111100"
        ALU.b_update(MBR.data)
        ALU.a_update(H.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.mbr_out1_start()
        CU.ui.mar_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mar_ld_update(ALU.out)
        MAR.load(ALU.out)
        #     enable ld of MDR and Tos is on bus
        ALU.controller = "010100"
        ALU.b_update(TOS.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.tos_out_start()
        CU.ui.mdr_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mdr_ld_update(ALU.out)
        MDR.load(ALU.out)
        CU.wr()

        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.sp_out_start()
        CU.ui.mar_ld_start()
        CU.ui.sp__ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mar_ld_update(ALU.out)
        CU.ui.sp__ld_update(ALU.out)
        MAR.load(ALU.out)
        SP.load(ALU.out)
        #     rd of memory
        CU.rd()

        #     enable ld of TOS and MDR is on bus
        ALU.controller = "010100"
        ALU.b_update(MDR.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.mdr_out_start()
        CU.ui.tos_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.tos_ld_update(ALU.out)
        TOS.load(ALU.out)
        CU.T = 0

    @staticmethod
    def ISUB():
        print("isub")
        CU.T += 1
        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.sp_out_start()
        CU.ui.mar_ld_start()
        CU.ui.sp__ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mar_ld_update(ALU.out)
        CU.ui.sp__ld_update(ALU.out)
        MAR.load(ALU.out)
        SP.load(ALU.out)
        #     rd of memory
        CU.rd()

        #     enable ld of H ,tos is on bus
        ALU.controller = "010100"
        ALU.b_update(TOS.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.tos_out_start()
        CU.ui.h_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.h_ld_update(ALU.out)
        H.load(ALU.out)
        # enable ld of tos and MDR
        ALU.controller = "111111"
        ALU.b_update(MDR.data)
        ALU.a_update(H.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.mdr_out_start()
        CU.ui.mdr_ld_start()
        CU.ui.tos_ld_start()
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.ui.mdr_ld_update(ALU.out)
        CU.ui.tos_ld_update(ALU.out)
        MDR.load(ALU.out)
        TOS.load(ALU.out)
        CU.wr()
        CU.T = 0

    @staticmethod
    def NOPE():
        print("nop")
        CU.T += 1
        # sys
        CU.flag = True
        while CU.flag:
            continue
        #
        CU.T = 0
