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
from graphics.UIs.ui import Ui_MainWindow


class CU:
    T = 0
    ui = Ui_MainWindow()
    flag = False

    @staticmethod
    def clocked():
        if CU.T == 0:
            CU.fetch()
        else:
            N = {0x10: CU.bipush(),
                 0xA7: CU.GOTO(),
                 0x60: CU.LADD(),
                 0x99: CU.IFEQ(),
                 0x9B: CU.IFLT(),
                 0x9F: CU.IF_ICMPEQ(),
                 0x84: CU.IINC(),
                 0x15: CU.ILOAD(),
                 0x36: CU.ISTORE(),
                 0x64: CU.ISUB(),
                 0x00: CU.NOPE(),
                 }[MBR.data]

    @staticmethod
    def fetch():

        ALU.controller = "110101"
        ALU.b_update(PC.data)

        # sys pause
        CU.ui.signals_stop()
        CU.ui.mbr_ld_start(Memory.read(PC.data))
        CU.ui.pc_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MBR.load(Memory.read(PC.data))
        PC.load(ALU.out)
        CU.T += 1

    @staticmethod
    def rd():
        #
        CU.ui.mdr_ld_start(Memory.read(MAR.data))
        #
        MDR.load(Memory.read(MAR.data))

    @staticmethod
    def wr():
        Memory.word_write(MDR.data, MAR.data)

    @staticmethod
    def bipush():
        # sp on bus to alu and enable sp ld

        ALU.controller = "110101"
        ALU.b_update(SP.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.sp_out_start()
        CU.ui.sp__ld_start(ALU.out)
        CU.ui.mar_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        SP.load(ALU.out)
        MAR.load(ALU.out)
        CU.fetch()
        # sys
        # b should be out of alu

        ALU.controller = "010100"
        ALU.b_update(MBR.data)
        # sys
        CU.ui.signals_stop()
        CU.ui.mdr_ld_start(ALU.out)
        CU.ui.tos_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #
        MDR.load(ALU.out)
        TOS.load(ALU.out)
        CU.wr()

    @staticmethod
    def GOTO():
        # ld of opc should be enabled and pc is on alu bus
        ALU.controller = "110110"
        ALU.b_update(PC.data)

        # sys
        CU.ui.signals_stop()
        CU.ui.opc_ld_start(ALU.out)
        CU.ui.mbr_out1_start()
        CU.flag = True
        while CU.flag:
            continue
        #

        OPC.load(ALU.out)
        CU.fetch()
        #     ld of H should be enabled
        ALU.controller = "011111"
        ALU.b_update(MBR.data)
        CU.fetch()

        # sys
        CU.ui.signals_stop()
        CU.ui.h_ld_start(ALU.out)
        CU.ui.mbr_out2_start()
        CU.flag = True
        while CU.flag:
            continue
        #

        H.load(ALU.out)
        ALU.controller = "011100"
        ALU.b_update(MBRU.data)     # todo in mbru chie??
        ALU.a_update(H.data)
        #     ld of H should be enabled

        # sys
        CU.ui.h_ld_start(ALU.out)
        CU.ui.opc_out_start()
        CU.flag = True
        while CU.flag:
            continue
        #

        H.load(ALU.out)
        ALU.controller = "111100"
        ALU.b_update(OPC.data)
        ALU.a_update(H.data)

        #     sys
        CU.ui.pc_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        PC.load(ALU.out)

    @staticmethod
    def LADD():
        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        #     sys
        CU.ui.mar_ld_start(ALU.out)
        CU.ui.sp__ld_start(ALU.out)
        CU.ui.sp_out_start()
        CU.flag = True
        while CU.flag:
            continue
        #

        MAR.load(ALU.out)
        SP.load(ALU.out)
        #     enable ld of H ,tos is on bus
        ALU.controller = "010100"
        ALU.b_update(TOS.data)

        #   sys
        CU.ui.tos_out_start()
        CU.ui.h_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        H.load(ALU.out)
        # enable ld of tos and MDR
        ALU.controller = "111100"
        ALU.b_update(MDR.data)
        ALU.a_update(H.data)

        #   sys
        CU.ui.mdr_out_start()
        CU.ui.mar_ld_start(ALU.out)
        CU.ui.tos_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MDR.load(ALU.out)
        TOS.load(ALU.out)
        CU.wr()

    @staticmethod
    def IFEQ():
        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        #     sys
        CU.ui.sp_out_start()
        CU.flag = True
        while CU.flag:
            continue
        #

        MAR.load(ALU.out)
        SP.load(ALU.out)
        # rd of memory is enabled

        CU.rd()
        #     enable ld of opc...tos is on bus

        ALU.controller = "010100"
        ALU.b_update(TOS.data)

        #   sys
        CU.ui.tos_out_start()
        CU.ui.opc_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        OPC.load(ALU.out)
        #   enable ld of tos and MDR is on bus
        ALU.controller = "010100"
        ALU.b_update(MDR.data)

        # sys
        CU.ui.mdr_out_start()
        CU.ui.tos_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        TOS.load(ALU.out)
        #     opc is on bus to check if it is zero
        ALU.controller = "010100"
        ALU.b_update(OPC.data)

        #     sys
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
            CU.ui.pc_out_start()
            CU.ui.opc_ld_start(ALU.out)
            CU.flag = True
            while CU.flag:
                continue
            #

            OPC.load(ALU.out)
            CU.GOTO()

        else:
            # ld pc enable to be incremented
            ALU.controller = "110101"
            ALU.b_update(PC.data)

            # sys pause
            CU.ui.pc_out_start()
            CU.ui.pc_ld_start(ALU.out)
            CU.flag = True
            while CU.flag:
                continue
            #

            PC.load(ALU.out)

            # ld pc enable to be incremented
            ALU.controller = "110101"
            ALU.b_update(PC.data)

            # sys pause
            CU.ui.pc_out_start()
            CU.ui.pc_ld_start(ALU.out)
            CU.flag = True
            while CU.flag:
                continue
            #

            PC.load(ALU.out)

    @staticmethod
    def IFLT():
        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        # sys
        CU.ui.sp_out_start()
        CU.ui.mar_ld_start(ALU.out)
        CU.ui.sp__ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MAR.load(ALU.out)
        SP.load(ALU.out)
        # rd of memory is enabled
        CU.rd()
        #     enable ld of opc...tos is on bus

        ALU.controller = "010100"
        ALU.b_update(TOS.data)

        # sys
        CU.ui.tos_out_start()
        CU.ui.opc_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        OPC.load(ALU.out)
        #   enable ld of tos and MDR is on bus
        ALU.controller = "010100"
        ALU.b_update(MDR.data)

        # sys
        CU.ui.mdr_out_start()
        CU.ui.tos_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        TOS.load(ALU.out)
        #     opc is on bus to check if it is zero
        ALU.controller = "010100"
        ALU.b_update(OPC.data)

        # sys
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
            CU.ui.pc_out_start()
            CU.ui.opc_ld_start(ALU.out)
            CU.flag = True
            while CU.flag:
                continue
            #

            OPC.load(ALU.out)
            CU.GOTO()

        else:
            # ld pc enable to be incremented
            ALU.controller = "110101"
            ALU.b_update(PC.data)

            # sys
            CU.ui.pc_out_start()
            CU.ui.pc_ld_start(ALU.out)
            CU.flag = True
            while CU.flag:
                continue
            #

            PC.load(ALU.out)

            # ld pc enable to be incremented
            ALU.controller = "110101"
            ALU.b_update(PC.data)

            # sys
            CU.ui.pc_out_start()
            CU.ui.pc_ld_start(ALU.out)
            CU.flag = True
            while CU.flag:
                continue
            #

            PC.load(ALU.out)

    @staticmethod
    def IF_ICMPEQ():
        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        # sys
        CU.ui.sp_out_start()
        CU.ui.mar_ld_start(ALU.out)
        CU.ui.sp__ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MAR.load(ALU.out)
        SP.load(ALU.out)
        # rd of memory is enabled
        CU.rd()
        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        # sys
        CU.ui.sp_out_start()
        CU.ui.sp__ld_start(ALU.out)
        CU.ui.mar_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MAR.load(ALU.out)
        SP.load(ALU.out)
        #     mdr is on bus and ld of H is enabled and rd of memory is enabled
        ALU.controller = "010100"
        ALU.b_update(H.data)

        # sys
        CU.ui.h_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        H.load(ALU.out)
        # rd of memory is enabled
        CU.rd()
        #     enable ld of opc...tos is on bus

        ALU.controller = "010100"
        ALU.b_update(TOS.data)

        # sys
        CU.ui.tos_out_start()
        CU.ui.opc_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        OPC.load(ALU.out)
        #   enable ld of tos and MDR is on bus
        ALU.controller = "010100"
        ALU.b_update(MDR.data)

        # sys
        CU.ui.mdr_out_start()
        CU.ui.tos_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        TOS.load(ALU.out)
        #     opc is on bus and alu is wants to have opc - H in the out
        ALU.controller = "111111"
        ALU.b_update(OPC.data)
        ALU.a_update(H.data)

        # sys
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
            CU.ui.pc_out_start()
            CU.ui.opc_ld_start(ALU.out)
            CU.flag = True
            while CU.flag:
                continue
            #

            OPC.load(ALU.out)
            CU.GOTO()

        else:
            # ld pc enable to be incremented
            ALU.controller = "110101"
            ALU.b_update(PC.data)

            # sys
            CU.ui.pc_out_start()
            CU.ui.pc_ld_start(ALU.out)
            CU.flag = True
            while CU.flag:
                continue
            #

            PC.load(ALU.out)

            # ld pc enable to be incremented
            ALU.controller = "110101"
            ALU.b_update(PC.data)

            # sys
            CU.ui.pc_out_start()
            CU.ui.pc_ld_start(ALU.out)
            CU.flag = True
            while CU.flag:
                continue
            #

            PC.load(ALU.out)

    @staticmethod
    def IINC():
        # در نظر گرفته که ابتدا varnumبیاد بعد const...هر دو رو هم یک بایتی در نظر گرفته
        CU.fetch()
        #     enable ld of H and LV is on bus
        ALU.controller = "010100"
        ALU.b_update(LV.data)

        # sys
        CU.ui.lv_out_start()
        CU.ui.h_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        H.load(ALU.out)
        #     enable ld of MAR and MBRU is on bus
        ALU.controller = "111100"
        ALU.b_update(MBR.data)
        ALU.a_update(H.data)

        # sys
        CU.ui.mbr_out1_start()
        CU.ui.mar_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MAR.load(ALU.out)
        CU.rd()
        CU.fetch()
        #     enable ld of H and MDR is on bus
        ALU.controller = "010100"
        ALU.b_update(MDR.data)

        # sys
        CU.ui.mdr_out_start()
        CU.ui.h_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        H.load(ALU.out)

        #     enable ld of MDR and MBR is on bus
        ALU.controller = "111100"
        ALU.b_update(MBR.data)
        ALU.a_update(H.data)

        # sys
        CU.ui.mbr_out1_start()
        CU.ui.mdr_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MDR.load(ALU.out)
        CU.wr()

    @staticmethod
    def ILOAD():
        # در نظر گرفته که ابتدا varnumبیاد بعد const...هر دو رو هم یک بایتی در نظر گرفته
        CU.fetch()
        #     enable ld of H and LV is on bus
        ALU.controller = "010100"
        ALU.b_update(LV.data)

        # sys
        CU.ui.lv_out_start()
        CU.ui.h_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        H.load(ALU.out)
        #     enable ld of MAR and MBRU is on bus
        ALU.controller = "111100"
        ALU.b_update(MBR.data)
        ALU.a_update(H.data)

        # sys
        CU.ui.mbr_out1_start()
        CU.ui.mar_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MAR.load(ALU.out)
        # ed of memory
        CU.rd()

        # ld of sp and MAR should be enabled and sp is on alu bus
        ALU.controller = "110101"
        ALU.b_update(SP.data)

        # sys
        CU.ui.sp_out_start()
        CU.ui.mar_ld_start(ALU.out)
        CU.ui.sp__ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MAR.load(ALU.out)
        SP.load(ALU.out)
        #     wr of memory
        CU.wr()
        #     enable ld of TOS and MDR is on bus
        ALU.controller = "010100"
        ALU.b_update(MDR.data)

        # sys
        CU.ui.mdr_out_start()
        CU.ui.tos_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        TOS.load(ALU.out)

    @staticmethod
    def ISTORE():
        # در نظر گرفته که ابتدا varnumبیاد بعد const...هر دو رو هم یک بایتی در نظر گرفته
        CU.fetch()
        #     enable ld of H and LV is on bus
        ALU.controller = "010100"
        ALU.b_update(LV.data)

        # sys
        CU.ui.lv_out_start()
        CU.ui.h_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        H.load(ALU.out)
        #     enable ld of MAR and MBRU is on bus
        ALU.controller = "111100"
        ALU.b_update(MBR.data)
        ALU.a_update(H.data)

        # sys
        CU.ui.mbr_out1_start()
        CU.ui.mar_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MAR.load(ALU.out)
        #     enable ld of MDR and Tos is on bus
        ALU.controller = "010100"
        ALU.b_update(TOS.data)

        # sys
        CU.ui.tos_out_start()
        CU.ui.mdr_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MDR.load(ALU.out)
        CU.wr()

        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        # sys
        CU.ui.sp_out_start()
        CU.ui.mar_ld_start(ALU.out)
        CU.ui.sp__ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MAR.load(ALU.out)
        SP.load(ALU.out)
        #     rd of memory
        CU.rd()

        #     enable ld of TOS and MDR is on bus
        ALU.controller = "010100"
        ALU.b_update(MDR.data)

        # sys
        CU.ui.mdr_out_start()
        CU.ui.tos_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        TOS.load(ALU.out)

    @staticmethod
    def ISUB():
        # ld of sp and MAR should be enabled and sp is on alu bus AND  rd of memory
        ALU.controller = "110110"
        ALU.b_update(SP.data)

        # sys
        CU.ui.sp_out_start()
        CU.ui.mar_ld_start(ALU.out)
        CU.ui.sp__ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MAR.load(ALU.out)
        SP.load(ALU.out)
        #     rd of memory
        CU.rd()

        #     enable ld of H ,tos is on bus
        ALU.controller = "010100"
        ALU.b_update(TOS.data)

        # sys
        CU.ui.tos_out_start()
        CU.ui.h_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        H.load(ALU.out)
        # enable ld of tos and MDR
        ALU.controller = "111111"
        ALU.b_update(MDR.data)
        ALU.a_update(H.data)

        # sys
        CU.ui.mdr_out_start()
        CU.ui.mdr_ld_start(ALU.out)
        CU.ui.tos_ld_start(ALU.out)
        CU.flag = True
        while CU.flag:
            continue
        #

        MDR.load(ALU.out)
        TOS.load(ALU.out)
        CU.wr()

    @staticmethod
    def NOPE():
        pass
