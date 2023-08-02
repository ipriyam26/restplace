from typing import Dict, List
from environment.state import EnvironmentState
from organism.organism import Organism
from organism.neural_network.actions import ActionComputation
from organism.neural_network.connection import Connection
from organism.sensory_input import SensoryComputation
import numpy as np


class Neuron:
    def __init__(self, neuron_id: str):
        self.neuron_id = neuron_id
        self.value = 0
        self.connections: List[Connection] = []

    def get_value(self):
        return self.value

    def add_connection(self, connection: Connection):
        self.connections.append(connection)


class SensoryNeuron(Neuron):
    def __init__(self, neuron_id: str, computation: SensoryComputation):
        super().__init__(neuron_id)
        self.computation = computation

    def update_value(self, organism: Organism, environment_state:EnvironmentState):
        self.value = self.computation.compute(organism, environment_state)


class InternalNeuron(Neuron):
    def __init__(self, neuron_id: str):
        super().__init__(neuron_id)

    def update_value(self, value_cache: Dict[str, float]):
        input_value = sum(
            connection.weight * value_cache[connection.source.neuron_id]
            for connection in self.connections
        )
        self.value = np.tanh(input_value)


class ActionNeuron(Neuron):
    def __init__(self, neuron_id: str, action_computation: ActionComputation):
        super().__init__(neuron_id)
        self.action_computation = action_computation

    def update_value(self, value_cache: Dict[str, float]):
        input_value = sum(
            connection.weight * value_cache[connection.source.neuron_id]
            for connection in self.connections
        )
        self.value = np.tanh(input_value)

    def get_action(self):
        return self.action_computation.compute(self.value)
