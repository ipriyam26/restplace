from organism.main import Organism


class Action:
    def perform(self, organism: Organism) -> bool:
        pass


class MovementAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def perform(self, organism: Organism) -> bool:
        # Update the organism's position based on the direction
        pass
