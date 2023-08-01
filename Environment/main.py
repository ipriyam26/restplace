from typing import List
from organism import Organism
from environment.state import EnvironmentState
from organism.main import PhysicalAttributes
from selection import SelectionStrategy


class Environment:
    def __init__(self, width: int, height: int, selection_strategy: SelectionStrategy):
        self.width = width
        self.height = height
        self.organisms: List[Organism] = []
        self.selection_strategy = selection_strategy
        self.environment_state = EnvironmentState(width=width, height=height)
        self.environment_state.update(self.get_attributes())

    def get_attributes(self) -> List[PhysicalAttributes]:
        return [organism.attributes for organism in self.organisms]

    def add_organism(self, organism: Organism):
        self.organisms.append(organism)

    def step(self):
        # Update state based on current state of environment
        self.environment_state.update(self.organisms)

        # Update each organism based on the state of the environment
        for organism in self.organisms:
            organism.step(self.environment_state)

        # Remove organisms that don't meet the selection criteria
        self.organisms = self.selection_strategy.select(self.organisms)
        self.environment_state.update(self.get_attributes())
 

    def get_state(self):
        return self.environment_state
