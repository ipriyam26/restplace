from typing import List
from selection.main import SelectionStrategy
from organism import Organism


class PositionSelectionStrategy(SelectionStrategy):
    def condition(self, organism: Organism) -> bool:
        pass

    def select(self, organisms: List[Organism]) -> List[Organism]:
        # Assuming the x and y position of the organism are stored in organism.position.x and organism.position.y
        # Organisms to the right of the line x=90 survive
        return [organism for organism in organisms if self.condition(organism)]
