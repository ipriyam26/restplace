from typing import Dict, List
from organism.main import Organism


class EnvironmentState:
    def __init__(self,length:int,width:int):
        self.board = [[0 for _ in range(width)] for _ in range(length)]


    def update(self, organisms:List[Organism]):
        self.board = [[0 for _ in range(len(self.board[0]))] for _ in range(len(self.board))]
        for organism in organisms:
            self.board[organism.x][organism.y] = organism.id

    def get_position(self):
        return self.positions
    
    def get_history(self):
        return self.history
    
    def get_history_of(self,organism_id:int):
        try:
            return self.history[organism_id]
        except KeyError as e:
            raise KeyError(f"Organism with id {organism_id} not found in history") from e
            