from Values import memory_size


class Memory:
    data = [0] * memory_size

    @staticmethod
    def clear():
        Memory.data = [0] * memory_size

    @staticmethod
    def byte_write(value, address):
        Memory.data[address] = value

    @staticmethod
    def word_write(value, address):
        Memory.data[address] = value % 2**8
        value //= 2**8
        Memory.data[address+1] = value % 2**8
        value //= 2**8
        Memory.data[address+2] = value % 2**8
        value //= 2**8
        Memory.data[address+3] = value

    @staticmethod
    def read(address):
        address = (address//4)*4
        return (Memory.data[address+3]*(2**24)) + (Memory.data[address+2]*(2**16)) + \
               (Memory.data[address+1]*(2**8)) + (Memory.data[address])
