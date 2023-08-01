from typing import Dict, List
from organism.main import Organism, PhysicalAttributes
import copy


class EnvironmentState:
    def __init__(self, width: int, height: int):
        self.board = [[None for _ in range(width)] for _ in range(height)]
        self.history: list[list[list[PhysicalAttributes|None]]] = []

    def update(self, attributes: List[PhysicalAttributes]):
        self.history.append(copy.deepcopy(self.board))
        self.board = [
            [None for _ in range(len(self.board[0]))] for _ in range(len(self.board))
        ]

        for organism in attributes:
            self.board[organism.y][organism.x] = organism

    def get_board(self):
        return self.board

    def get_history(self):
        return self.history