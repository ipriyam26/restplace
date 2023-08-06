import itertools
from typing import Dict, List
from organism.organism import PhysicalAttributes
import copy
from config import POPULATION_RANGE_FORWARD
from utils.types import Cordinates


class EnvironmentState:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [[None for _ in range(width)] for _ in range(height)]
        self.history: list[list[list[PhysicalAttributes | None]]] = []
        self.gradient_board = [[0.0 for _ in range(width)] for _ in range(height)]
        self.population_board = [[0 for _ in range(width)] for _ in range(height)]
        self.orgnaisms_history: Dict[int, List[PhysicalAttributes]] = {}
        self.step_count = (0,)
        self.last_movement: Dict[int, Cordinates] = {}
        self.blockage_board_long = [[0.0 for _ in range(width)] for _ in range(height)]
        self.blockage_board = [[0.0 for _ in range(width)] for _ in range(height)]
        self.population_gradient_board_left_right = [
            [0.0 for _ in range(len(self.board[0]))] for _ in range(len(self.board))
        ]
        self.population_gradient_board_north_south = [
            [0.0 for _ in range(len(self.board[0]))] for _ in range(len(self.board))
        ]

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
        self.compute_last_movement()
        self.compute_blockage_forward()
        self.compute_blockage_left_right()
        self.compute_population_gradient_left_right()
        self.compute_population_gradient_north_south()
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

    # compute last movement X and Y for all organisms
    def compute_last_movement(self):
        last_movement = self.orgnaisms_history[self.step_count - 1]
        current_movement = self.orgnaisms_history[self.step_count]
        for last, current in zip(last_movement, current_movement):
            self.last_movement[current.id] = Cordinates(
                current.x - last.x, current.y - last.y
            )
        return self.last_movement

    def compute_blockage_forward(self):
        self.blockage_board_long = [
            [0 for _ in range(len(self.board[0]))] for _ in range(len(self.board))
        ]
        range_length = 8

        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                blockage = next(
                    (
                        1
                        for forward_x in range(1, range_length + 1)
                        if x + forward_x < len(self.board[0])
                        and self.board[y][x + forward_x] is not None
                    ),
                    0,
                )
                self.blockage_board_long[y][x] = blockage

        return self.blockage_board_long

    def compute_blockage_left_right(self):
        self.blockage_board = [
            [0 for _ in range(len(self.board[0]))] for _ in range(len(self.board))
        ]

        for y, x in itertools.product(
            range(len(self.board)), range(len(self.board[0]))
        ):
            left_blockage = x > 0 and self.board[y][x - 1] is not None
            right_blockage = (
                x < len(self.board[0]) - 1 and self.board[y][x + 1] is not None
            )

            blockage = int(left_blockage or right_blockage)
            self.blockage_board[y][x] = blockage

        return self.blockage_board

    def compute_population_gradient_left_right(self):
        self.population_gradient_board_left_right = [
            [0.0 for _ in range(len(self.board[0]))] for _ in range(len(self.board))
        ]

        # Scale the gradient to be between -4 and 4
        max_gradient = 1  # assuming the ratio can't be greater than 1
        for y, x in itertools.product(
            range(len(self.board)), range(len(self.board[0]))
        ):
            left_population = sum(self.board[y][i] is not None for i in range(x))
            right_population = sum(
                self.board[y][i] is not None for i in range(x + 1, len(self.board[0]))
            )

            left_available_cells = x
            right_available_cells = len(self.board[0]) - x - 1

            left_ratio = (
                left_population / left_available_cells
                if left_available_cells != 0
                else 0
            )
            right_ratio = (
                right_population / right_available_cells
                if right_available_cells != 0
                else 0
            )
            gradient = right_ratio - left_ratio
            self.population_gradient_board_left_right[y][x] = gradient * 4

        return self.population_gradient_board_left_right

    def compute_population_gradient_north_south(self):
        self.population_gradient_board_north_south = [
            [0.0 for _ in range(len(self.board[0]))] for _ in range(len(self.board))
        ]

        for y, x in itertools.product(
            range(len(self.board)), range(len(self.board[0]))
        ):
            north_population = sum(self.board[i][x] is not None for i in range(y))
            south_population = sum(
                self.board[i][x] is not None for i in range(y + 1, len(self.board))
            )

            north_available_cells = y
            south_available_cells = len(self.board) - y - 1

            north_ratio = (
                north_population / north_available_cells
                if north_available_cells != 0
                else 0
            )
            south_ratio = (
                south_population / south_available_cells
                if south_available_cells != 0
                else 0
            )

            gradient = south_ratio - north_ratio

            self.population_gradient_board_north_south[y][x] = gradient * 4
        return self.population_gradient_board_north_south

    def get_board(self):
        return self.board

    def get_history(self):
        return self.history
