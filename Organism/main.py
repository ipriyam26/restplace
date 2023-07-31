from dataclasses import dataclass
from organism.neural_network.brain import NeuralNetwork

@dataclass
class PhysicalAttributes:
    x: int
    y: int
    pheronome: float
    oscillator: float
    genome:str
    age:int
    id:int

class Organism:
    def __init__(self, x:int, y:int,id:int,genome:str):
        self.neural_network = NeuralNetwork()
        self.id = id
        self.attributes = PhysicalAttributes(x=x,y=y,pheronome=0,oscillator=0,genome=genome,age=0,id=id)

    def step(self, environment):
        self.neural_network.process(organism=self, environment=environment)

        # Select the ActionNeuron with the highest value
        max_value = -float('inf')
        best_action = None
        for action_neuron in self.neural_network.action_neurons:
            if action_neuron.get_value() > max_value:
                max_value = action_neuron.get_value()
                best_action = action_neuron.get_action()
        
        if best_action:
            best_action.perform(self)





