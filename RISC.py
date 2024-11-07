class RISCProcessor:
    def __init__(self, memory_size=256, num_registers=8):
        # Memória do processador e registradores
        self.memory = [0] * memory_size
        self.registers = [0] * num_registers
        self.pc = 0  # Contador de Programa (Program Counter)
        self.running = True  # Estado de execução do processador

    def load_program(self, program):
        # Carrega um programa (lista de instruções) na memória
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def fetch(self):
        # Busca a instrução da memória e incrementa o PC
        instruction = self.memory[self.pc]
        self.pc += 1
        return instruction

    def decode_execute(self, instruction):
        # Decodifica e executa a instrução
        opcode, *args = instruction

        if opcode == "LOAD":
            reg, addr = args
            self.registers[reg] = self.memory[addr]

        elif opcode == "STORE":
            reg, addr = args
            self.memory[addr] = self.registers[reg]

        elif opcode == "ADD":
            reg1, reg2 = args
            self.registers[reg1] += self.registers[reg2]

        elif opcode == "SUB":
            reg1, reg2 = args
            self.registers[reg1] -= self.registers[reg2]

        elif opcode == "JMP":
            addr = args[0]
            self.pc = addr

        elif opcode == "BEQ":
            reg1, reg2, addr = args
            if self.registers[reg1] == self.registers[reg2]:
                self.pc = addr

        elif opcode == "HLT":
            self.running = False  # Instrução para parar o processador

    def run(self):
        # Executa o ciclo do processador até que o programa pare
        while self.running:
            instruction = self.fetch()
            self.decode_execute(instruction)
            self.debug_state()  # Debug: exibir o estado atual do processador

    def debug_state(self):
        # Exibe o estado atual dos registradores e do PC
        print(f"PC: {self.pc}, Registers: {self.registers}, Memory: {self.memory[:10]}")  # Exibe os primeiros 10 endereços

# Programa exemplo para teste
# Formato das instruções: [opcode, operando1, operando2, ...]
program = [
    ("LOAD", 0, 10),   # R0 = Mem[10]
    ("LOAD", 1, 11),   # R1 = Mem[11]
    ("ADD", 0, 1),     # R0 = R0 + R1
    ("STORE", 0, 12),  # Mem[12] = R0
    ("SUB", 0, 1),     # R0 = R0 - R1
    ("BEQ", 0, 1, 8),  # Se R0 == R1, salta para a instrução na posição 8
    ("JMP", 9),        # Salta incondicional para a posição 9
    ("HLT",),          # Parar o programa
]

# Carregando dados iniciais na memória para teste
processor = RISCProcessor()
processor.memory[10] = 5   # Valor inicial na posição de memória 10
processor.memory[11] = 10  # Valor inicial na posição de memória 11

# Carregando e executando o programa
processor.load_program(program)
processor.run()
