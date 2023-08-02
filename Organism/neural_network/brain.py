from typing import Any, Dict, List
from environment.state import EnvironmentState
from organism.organism import Organism
from organism.neural_network.connection import Connection
from organism.neural_network.neuron import (
    ActionNeuron,
    InternalNeuron,
    SensoryNeuron,
)
from organism.neural_network.gene import Gene
from config import INTERNAL_NEURON_COUNT


class NeuralNetwork:
    def __init__(self, genome: List[str], max_iterations=100):
        self.__make_neurons()
        self.genome = genome
        self.genes = [Gene.from_hex(gene) for gene in genome]
        connections = [
            gene.parse(
                num_sensory_neurons=len(self.sensory_neurons),
                num_internal_neurons=len(self.internal_neurons),
                num_action_neurons=len(self.action_neurons),
            )
            for gene in self.genes
        ]

        self.add_connection(connections)

        self.max_iterations = max_iterations

    def add_connection(self, connections: list[dict[str, Any]]):
        for conn in connections:
            source_type: str = conn["source_type"]
            source_id: int = conn["source_id"]
            sink_type: str = conn["sink_type"]
            sink_id: int = conn["sink_id"]
            weight: float = conn["weight"]

            if source_type == "sensory":
                source = self.sensory_neurons.get(source_id)
            elif source_type == "internal":
                source = self.internal_neurons.get(source_id)

            if sink_type == "internal":
                sink = self.internal_neurons.get(sink_id)
            elif sink_type == "action":
                sink = self.action_neurons.get(sink_id)
            connection = Connection(source=source, sink=sink, weight=weight)
            source.add_connection(connection)

    def __make_neurons(self):
        self.sensory_neurons = self.__make_sensory_neuron()
        self.internal_neurons = self.__make_internal_neuron()
        self.action_neurons = self.__make_action_neuron()

    def __make_sensory_neuron(self) -> Dict[int, SensoryNeuron]:
        pass

    def __make_internal_neuron(self) -> Dict[int, InternalNeuron]:
        start_id = self.sensory_neurons[-1].neuron_id + 1
        return {
            i + start_id: InternalNeuron(neuron_id=i + start_id)
            for i in range(INTERNAL_NEURON_COUNT)
        }

    def __make_action_neuron(self) -> Dict[int, ActionNeuron]:
        # start_id = self.internal_neurons[-1].neuron_id + 1
        pass

    # #TODO: Implement this
    #     @classmethod
    #     def from_genome(cls, genome:List[str]):
    #         genes = [Gene.from_hex(gene) for gene in genome]
    #         for gene in genes:
    #             conn = gene.parse()

    def process(self, organism: Organism, environment_state: EnvironmentState):
        # Update sensory neurons
        for _,neuron in self.sensory_neurons.items():
            neuron.update_value(organism, environment_state)

        # Update internal neurons until values stabilize
        for _ in range(self.max_iterations):
            value_cache = {
                neuron.neuron_id: neuron.get_value() for _,neuron in self.internal_neurons.items()
            }
            change_occurred = False
            for neuron in self.internal_neurons:
                old_value = value_cache[neuron.neuron_id]
                neuron.update_value(value_cache)
                if neuron.get_value() != old_value:
                    change_occurred = True
            if not change_occurred:
                break

        # Update action neurons
        value_cache = {
            neuron.neuron_id: neuron.get_value() for neuron in self.internal_neurons
        }
        for neuron in self.action_neurons:
            neuron.update_value(value_cache)
