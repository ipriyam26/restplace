from typing import Dict, List
from organism.main import Organism


class EnvironmentState:
    def __init__(self):
        self.history:Dict[int,List[tuple[int,int]]]={}
        self.positions:Dict[int, tuple[int, int]] = {}

    def update(self, organisms:List[Organism]):
        # Update positions based on the current state of the organisms
        self.positions = {organism.id: (organism.x,organism.y) for organism in organisms}
        #for each organism update the history of positions of each organism, i.e add then to a list
        for organism in organisms:
            old_value = self.history.get(organism.id,[])
            self.history[organism.id] = old_value + [(organism.x,organism.y)]

    def get_position(self):
        return self.positions
    
    def get_history(self):
        return self.history
    
    def get_history_of(self,organism_id:int):
        try:
            return self.history[organism_id]
        except KeyError as e:
            raise KeyError(f"Organism with id {organism_id} not found in history") from e
            