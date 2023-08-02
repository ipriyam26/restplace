import itertools
from typing import List
from organism.organism import PhysicalAttributes
import copy
from config import POPULATION_RANGE_FORWARD


class EnvironmentState:
    def __init__(self, width: int, height: int):
        self.board = [[None for _ in range(width)] for _ in range(height)]
        self.history: list[list[list[PhysicalAttributes | None]]] = []
        self.gradient_board = [[0.0 for _ in range(width)] for _ in range(height)]
        self.population_board = [[0 for _ in range(width)] for _ in range(height)]
        self.orgnaisms_history = {}
        self.step_count = 0

    def update(self, attributes: List[PhysicalAttributes]):
        self.orgnaisms_history[self.step_count] = copy.deepcopy(attributes)
        self.history.append(copy.deepcopy(self.board))
        self.board = [
            [None for _ in range(len(self.board[0]))] for _ in range(len(self.board))
        ]

        for organism in attributes:
            self.board[organism.y][organism.x] = organism
        self.compute_pheromone_gradient()
        self.compute_population_board()
        self.step_count += 1

    def compute_pheromone_gradient(self):
        for y, x in itertools.product(
            range(len(self.board)), range(len(self.board[0]))
        ):
            left_pheromone = self.board[y][x - 1].pheromone if x > 0 else 0
            right_pheromone = (
                self.board[y][x + 1].pheromone if x < len(self.board[0]) - 1 else 0
            )
            self.gradient_board[y][x] = right_pheromone - left_pheromone

    def compute_population_board(self):
        range_forward = POPULATION_RANGE_FORWARD
        for y in range(len(self.board)):
            count = 0
            for x in range(len(self.board[0]) - 1, -1, -1):
                if x < len(self.board[0]) - range_forward:
                    count -= 1 if self.board[y][x + range_forward] is not None else 0
                if self.board[y][x] is not None:
                    count += 1

                self.population_board[y][x] = count

    def get_board(self):
        return self.board

    def get_history(self):
        return self.history
