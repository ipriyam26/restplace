from dataclasses import dataclass
from typing import List
from organism.neural_network.brain import NeuralNetwork
from organism.neural_network.gene import Gene


@dataclass
class PhysicalAttributes:
    x: int
    y: int
    pheronome: float
    oscillator: float
    genome: str
    age: int
    id: int
    genes: List[Gene]


class Organism:
    def __init__(self, x: int, y: int, id: int, genome: List[str]):
        self.neural_network = NeuralNetwork(genome=genome)
        self.id = id
        self.attributes = PhysicalAttributes(
            x=x,
            y=y,
            pheronome=0,
            oscillator=0,
            genome=genome,
            age=0,
            id=id,
            genes=self.neural_network.genes,
        )

    def step(self, environment):
        self.neural_network.process(organism=self, environment=environment)

        # Select the ActionNeuron with the highest value
        max_value = -float("inf")
        best_action = None
        for action_neuron in self.neural_network.action_neurons:
            if action_neuron.get_value() > max_value:
                max_value = action_neuron.get_value()
                best_action = action_neuron.get_action()

        if best_action:
            best_action.perform(self)
