from Values import asm_opened, asm_path, instruction_dic, instruction_operands


def undefined_instruction(wrong_word, line_number_in_raw_file):
    print(wrong_word, line_number_in_raw_file)
    # todo: change to raise an exception


def assemble():
    instructions_file = open("codes/assembled/instructions.txt", "w")
    constants_file = open("codes/assembled/constants.txt", "w")
    local_vars_file = open("codes/assembled/local_vars.txt", "w")
    instructions_string = ""
    constants_string = ""
    local_vars_string = ""
    const_table = []
    vars_table = []
    labels = {}
    if asm_opened:
        raw_asm = open(asm_path, "r").read().split("\n")
    else:
        raw_asm = open("codes/deafult_input_assembly.txt", "r").read().split("\n")

    # find file segments
    text_index = raw_asm.index(".text")
    const_index = raw_asm.index(".consts")
    vars_index = raw_asm.index(".vars")
    text_index_end = raw_asm.index(".end_text")
    const_index_end = raw_asm.index(".end_consts")
    vars_index_end = raw_asm.index(".end_vars")

    # split segments
    text_seg = raw_asm[text_index+1: text_index_end]
    const_seg = raw_asm[const_index+1: const_index_end]
    vars_seg = raw_asm[vars_index+1: vars_index_end]

    # todo correct this block
    # finding labels
    # for index in range(len(text_seg)):
    #     key = text_seg[index]
    #     if key.endswith(":"):
    #         labels.update({key, index})

    # relocating
    for const in const_seg:
        key, value = const.split()
        const_table.append(key)
        constants_string += value
        constants_string += "\n"
    for var in vars_seg:
        key, value = var.split()
        vars_table.append(key)
        local_vars_string += value
        local_vars_string += "\n"

    # todo remaining codes should be replaced by a code supports labels
    for instruction in text_seg:
        opcode = instruction.split()[0]
        if instruction.startswith("#"):
            continue
        if instruction.endswith(":"):
            labels.update({instruction, text_seg.index(instruction)})
        if opcode not in list(instruction_dic.keys()):
            undefined_instruction(opcode, text_seg.index(instruction) + text_index)
        hex_opcode = instruction_dic[opcode]
        instructions_string += hex(hex_opcode)[2:]
        instructions_string += "\n"
        if instruction_operands[opcode] > 0:
            operand = instruction.split()[1]
            if hex_opcode == instruction_dic["bipush"]:
                if operand.endswith("h") or operand.endswith("H")or operand.endswith("x")or operand.endswith("X"):
                    instructions_string += operand[:-1]
                    instructions_string += "\n"
                elif operand.endswith("b") or operand.endswith("B"):
                    instructions_string += hex(int(operand[:-1], 2))[2:]
                    instructions_string += "\n"
                else:
                    instructions_string += hex(int(operand))[2:]
                    instructions_string += "\n"
            elif hex_opcode == instruction_dic["goto"]:
                instructions_string += hex(labels[operand] - text_seg.index(instruction))[2:]
                instructions_string += "\n"
            elif hex_opcode == instruction_dic["ifeq"]:
                instructions_string += hex(labels[operand] - text_seg.index(instruction))[2:]
                instructions_string += "\n"
            elif hex_opcode == instruction_dic["iflt"]:
                instructions_string += hex(labels[operand] - text_seg.index(instruction))[2:]
                instructions_string += "\n"
            elif hex_opcode == instruction_dic["if_icmpeq"]:
                instructions_string += hex(labels[operand] - text_seg.index(instruction))[2:]
                instructions_string += "\n"
            elif hex_opcode == instruction_dic["iinc"]:
                instructions_string += hex(vars_table.index(operand))
                instructions_string += "\n"
                operand2 = instruction.split()[2]
                instructions_string += hex(const_table.index(operand2))
                instructions_string += "\n"
            elif hex_opcode == instruction_dic["iload"]:
                instructions_string += hex(vars_table.index(operand))
                instructions_string += "\n"
            elif hex_opcode == instruction_dic["istore"]:
                instructions_string += hex(vars_table.index(operand))
                instructions_string += "\n"
    constants_file.write(constants_string)
    local_vars_file.write(local_vars_string)
    instructions_file.write(instructions_string)
