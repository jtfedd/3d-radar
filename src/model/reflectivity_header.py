class ReflectivityHeader:
    def __init__(self, level2Ray):
        header = level2Ray[4][b"REF"][0]
        self.numGates = header.num_gates
        self.gateWidth = header.gate_width
        self.firstGate = header.first_gate

    def range(self, i):
        return self.firstGate + (self.gateWidth * i)
