from codes.assembler import assemble


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


def run_btn_clicked():
    print("6")
    pass


def step_fwd_btn_clicked():
    print("7")
    pass


def clear_btn_clicked():
    pass
