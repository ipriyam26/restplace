class Action:
    def perform(self, organism):
        pass

class MovementAction(Action):
    def __init__(self, direction):
        self.direction = direction

    def perform(self, organism):
        # Update the organism's position based on the direction
        pass
