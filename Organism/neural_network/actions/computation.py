from abc import ABC, abstractmethod

from organism.neural_network.actions.action import MovementAction, Action

class ActionComputation(ABC):
    @abstractmethod
    def compute(self, neuron_value:float)->Action:
        pass
class MovementActionComputation(ActionComputation):
    def compute(self, neuron_value)->Action:
        # Translate neuron value into a movement action
        # This is a placeholder implementation
        return MovementAction(direction=neuron_value)


