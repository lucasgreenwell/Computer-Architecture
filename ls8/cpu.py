"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #ram
        self.ram = [0] * 256
        #registers
        self.reg = [0] * 8
        #pointer/ program counter
        self.pc =  0
        #flags register
        self.flags = [0] * 8


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0
        with open(sys.argv[1]) as f:
            #iterate through each line in the given file
            for line in f:
                #clean the instruction
                instruction = line.split("#")[0].strip()
                #avoid empty lines and bullshit after hashtags
                if instruction == '':
                    continue
                #convert from binary because binary is weird
                value = int(instruction, 2)
                #put that shit in the ram, not using my read or writes because they're fucking up my life
                self.ram[address] = value
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            #then add
            self.reg[reg_a] += self.reg[reg_b]
        if op == "SUB":
            #then subtract
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

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
        LDI = 0b10000010
        HLT = 0b00000001
        PRN = 0b01000111
        MUL = 0b10100010
        SUB = 10100001
        ADD = 10100000
        PUSH = 0b01000101
        POP = 0b01000110
        SP = 7
        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110
        JMP = 0b01010100



        running = True
        #i don't understand why this needs to be there
        self.reg[SP] = 0xF4
        i = 0
        while running:
            i += 1
            print(f'iteration {i}')
            ir = self.ram[self.pc]
            #print(IR, self.pc)
            if ir == HLT:
                running = False

            elif ir == CMP:
                print('cmp happens')
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                if self.reg[operand_a] is self.reg[operand_b]:
                    self.flags[-1] = 1
                elif self.reg[operand_a] > self.reg[operand_b]:
                    self.flags[-2] = 1
                else:
                    self.flags[-3] = 1
                self.pc += 3

            elif ir == JEQ:
                print('jeq happens')
                operand_a = self.ram[self.pc + 1]
                if self.flags[-1] is 1:
                    self.pc = self.reg[self.ram[self.pc + 1]]
                self.pc += 2

            elif ir == JNE:
                print('jne happens')
                operand_a = self.ram[self.pc + 1]
                if self.flags[-1] == 0:
                    self.pc = self.reg[self.ram[self.pc + 1]]
                self.pc += 2

            elif ir == JMP:
                print('jmp happens')
                self.pc = self.reg[self.ram[self.pc + 1]]
                # operand_a = self.ram[self.pc + 1]
                # self.pc = operand_a

            elif ir == LDI:
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == PRN:
                operand_a = self.ram[self.pc + 1]
                print(self.reg[operand_a])
                self.pc += 2

            elif ir == MUL:
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                #grab the values and send em through the alu
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif ir == SUB:
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                #grab the values and send em through the alu
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif ir == ADD:
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                #grab the values and send em through the alu
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3

            elif ir == PUSH:
                print('pushing')
                #lower the stack pointer
                self.reg[SP] -= 1
                #get the register
                operand_a = self.ram[self.pc + 1]
                #value in the register
                value = self.reg[operand_a]
                #take the value from the register and put it on top of the stack
                top_of_stack = self.reg[SP]
                # print(top_of_stack)
                self.ram[top_of_stack] = value
                self.pc += 2
                # print('other', operand_a)
                # print('thing', value)

            elif ir == POP:
                print('popping')
                #raise the stack pointer
                self.reg[SP] += 1
                self.pc += 2
                #take the thing on top of the stack off
                top_of_stack = self.reg[SP]
                self.ram[top_of_stack] = 0
                # print(self.reg[SP])

            # elif ir is JEQ :
            #     print('not sure what to do')
            else:
                print('unknown instruction', ir)
                sys.exit(1)




