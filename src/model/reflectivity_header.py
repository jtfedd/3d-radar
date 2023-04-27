class ReflectivityHeader:
    @classmethod
    def fromLevel2Data(cls, level2Ray):
        header = level2Ray[4][b'REF'][0]
        return cls(header.num_gates, header.gate_width, header.first_gate)

    def __init__(self, numGates, gateWidth, firstGate):
        self.numGates = numGates
        self.gateWidth = gateWidth
        self.firstGate = firstGate

    def range(self, i):
        return self.firstGate + (self.gateWidth * i)