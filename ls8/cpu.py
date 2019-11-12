"""CPU functionality."""

import sys



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # allocate 256 bytes of memory
        self.pc = 0
        self.reg = [0] * 8
        self.fl = 0
        self.HLT = 0b00000001
        self.PRN = 0b01000111
        self.LDI = 0b10000010

    def ram_read(self, MAR):
        value = self.ram[MAR]
        return value

    def ram_write(self, address, MDR):
        self.ram[address] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        halted = False
        while not halted:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == self.LDI:
                # Set the value of a register to an integer.
                register_index = operand_a
                self.reg[register_index] = operand_b
                self.pc += 3
            # elif IR == OPCODES.NOP.code:
            #     self.pc += 1
            elif IR == self.PRN:
                # Print numeric value stored in the given register.
                # Print to the console the decimal integer value that is stored in the given
                # register.
                reg_index = operand_a
                value = int(self.reg[reg_index])
                print(f'{value}')
                self.pc += 2
            elif IR == self.HLT:
                halted = True
                self.pc += 1
            else:
                print(f'Unknown instruction at index {self.pc}')
                self.pc += 1
