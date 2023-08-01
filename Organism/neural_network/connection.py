from organism.neural_network.neuron import Neuron


class Connection:
    def __init__(self, source: Neuron, sink: Neuron, weight: float):
        self.source = source
        self.sink = sink
        self.weight = weight
