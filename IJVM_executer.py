def memory_initialization():
    instructions = open("codes/assembled/instructions.txt", "r").read().split()
    constants = open("codes/assembled/constants.txt", "r").read().split()
    local_vars = open("codes/assembled/local_vars.txt", "r").read().split()
    instructions = map(lambda q: int(q, 16), instructions)
    constants = map(lambda q: int(q, 16), constants)
    local_vars = map(lambda q: int(q, 16), local_vars)

