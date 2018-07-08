# assembly file
asm_saved = False
asm_opened = False
asm_path = "default"

# instructions
instruction_dic = {"bipush": 0x10,
                   "goto": 0xA7,
                   "iadd": 0x60,
                   "ifeq": 0x99,
                   "iflt": 0x9B,
                   "if_icmpeq": 0x9F,
                   "iinc": 0x84,
                   "iload": 0x15,
                   "istore": 0x36,
                   "isub": 0x64,
                   "nop": 0x00}
instruction_operands = {"bipush": 1,
                        "goto": 1,
                        "iadd": 0,
                        "ifeq": 1,
                        "iflt": 1,
                        "if_icmpeq": 1,
                        "iinc": 2,
                        "iload": 1,
                        "istore": 1,
                        "isub": 0,
                        "nop": 0}

# memory:
memory_size = 2 ** 16

# registers default value
PC_default = 0
SP_default = 0
LV_default = 0
CPP_default = 0
