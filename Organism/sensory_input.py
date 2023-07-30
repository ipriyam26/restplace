from abc import ABC, abstractmethod

class SensoryComputation(ABC):
    @abstractmethod
    def compute(self, organism, environment):
        pass

class ComputeSIr(SensoryComputation):
    def compute(self, organism, environment):
        # Implement the computation for SIr here.
        pass

class ComputeLPf(SensoryComputation):
    def compute(self, organism, environment):
        # Implement the computation for LPf here.
        pass