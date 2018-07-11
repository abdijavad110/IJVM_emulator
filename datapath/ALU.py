class ALU:
    controller = "010000"
    A = 0
    B = 0
    out = 0
    Z=0
    N=0
    @staticmethod
    def update():
        ALU.out = {
            "011000": ALU.A,
            "010100": ALU.B,
            "011010": ~ALU.A,
            "101100": ~ALU.B,
            "111100": ALU.A + ALU.B,
            "111101": ALU.A + ALU.B + 1,
            "111001": ALU.A + 1,
            "110101": ALU.B + 1,
            "111111": ALU.B - ALU.A,
            "110110": ALU.B - 1,
            "111011": -ALU.A,
            "001100": ALU.A & ALU.B,
            "011100": ALU.A | ALU.B,
            "010000": 0,
            "110001": 1,
            "110010": -1,
            "011111": ALU.B << 8

        }[ALU.controller]
        if ALU.out >= 4294967296:
            ALU.out = ALU.out & 4294967295
        ALU.Z= 1 if ALU.out==0 else 0
        ALU.N= 1 if ALU.out<0 else 0
    @staticmethod
    def a_update(a):
        ALU.A = a
        ALU.update()

    @staticmethod
    def b_update(b):
        ALU.B = b
        ALU.update()

    @staticmethod
    def controller_update(value):
        ALU.controller = value
        ALU.update()
