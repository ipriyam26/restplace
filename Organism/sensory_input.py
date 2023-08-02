from abc import ABC, abstractmethod
from environment.state import EnvironmentState

from organism.organism import Organism


class SensoryComputation(ABC):
    @abstractmethod
    def compute(self, organism: Organism, environment_state: EnvironmentState) -> float:
        pass


class ComputePhlr(SensoryComputation):
    """
    Sensory Neuron Computation that calculates the pheromone gradient at the organism's current location. The gradient is retrieved from the
    environment's current state.

    This class is a derived class of the `SensoryComputation` base class.
    """

    def compute(self, organism: Organism, environment_state: EnvironmentState) -> float:
        """
        Computes pheromone gradient at the organism's current location from
        the `gradient_board` of the given `EnvironmentState`.

        Parameters:
        ----------
        organism: Organism
            The organism for which to compute the pheromone gradient.

        environment_state: EnvironmentState
            The current state of the environment, which holds the gradient board.

        Returns:
        -------
        float
            The pheromone gradient at the organism's current location.
        """

        return environment_state.gradient_board[organism.attributes.y][
            organism.attributes.x
        ]


class ComputePLR(SensoryComputation):
    """Sensory Neuron Computation that calculates the population in the long range forward direction. The population is retrieved from the environment's current state.

    This class is a derived class of the `SensoryComputation` base class.
    """
    def compute(self, organism: Organism, environment_state: EnvironmentState) -> float:
        """
        Compute the long-range forward population count for a given organism.

        The count is calculated as the number of organisms present within a given 
        range ahead on the x-axis. If the position is outside the board, it is not 
        counted.

        Parameters:
        ----------
        organism: Organism
            The organism for which to compute the long-range forward population count.

        environment_state: EnvironmentState
            The current state of the environment, which holds the population board.

        Returns:
        -------
        float
            The long-range forward population count for the given organism.
        """
        return environment_state.population_board[organism.attributes.y][
            organism.attributes.x
        ]



# SENSORY INPUTS
# SIr = pheromone gradient left-right
# LPf = population long-range forward
# Sfd = pheromone gradient forward
# LMy = last movement Y
# Sg = pheromone density
# LBf = blockage long-range forward
# Age = age
# LMx = last movement X
# Rnd = random input
# BDy = north/south border distance
# BIr = blockage left-right
# Gen = genetic similarity of fwd neighbor
# Osc = oscillator
# BDx = east/west border distance
# Bfd = blockage forward
# Lx = east/west world location
# PIr = population gradient left-right
# BD = nearest border distance
# Pop = population density
# Ly = north/south world location
# Pfd = population gradient forward
