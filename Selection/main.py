from abc import ABC, abstractmethod
from typing import List
from organism import Organism

class SelectionStrategy(ABC):
    @abstractmethod
    def select(self, organisms: List[Organism]) -> List[Organism]:
        pass
