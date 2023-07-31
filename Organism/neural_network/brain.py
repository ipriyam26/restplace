from typing import List
from organism.main import Organism
from organism.neural_network.connection import Connection
from organism.neural_network.neuron import ActionNeuron, InternalNeuron, Neuron, SensoryNeuron


class NeuralNetwork:
    def __init__(self, neurons:List[Neuron], connections:List[Connection], max_iterations=100):
        for conn in connections:
            self.neurons[conn.sink.neuron_id].add_connection(conn)
        self.max_iterations = max_iterations
        self.sensory_neurons = [neuron for neuron in neurons if isinstance(neuron, SensoryNeuron)]
        self.internal_neurons = [neuron for neuron in neurons if not isinstance(neuron, InternalNeuron)]
        self.action_neurons = [neuron for neuron in neurons if isinstance(neuron, ActionNeuron)]

    @classmethod
    def from_genome(cls, genome:str):
        pass


    def process(self, organism:Organism, environment):

        # Update sensory neurons
        for neuron in self.sensory_neurons:
            neuron.update_value(organism, environment)
        
        # Update internal neurons until values stabilize
        for _ in range(self.max_iterations):
            value_cache = {neuron.neuron_id: neuron.get_value() for neuron in self.internal_neurons}
            change_occurred = False
            for neuron in self.internal_neurons:
                old_value = value_cache[neuron.neuron_id]
                neuron.update_value(value_cache)
                if neuron.get_value() != old_value:
                    change_occurred = True
            if not change_occurred:
                break
        
        # Update action neurons
        value_cache = {neuron.neuron_id: neuron.get_value() for neuron in self.internal_neurons}
        for neuron in self.action_neurons:
            neuron.update_value(value_cache)

