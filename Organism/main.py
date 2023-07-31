from organism.neural_network.brain import NeuralNetwork

class Organism:
    def __init__(self, x:int, y:int, neural_network: NeuralNetwork,id:int):
        self.x = x
        self.y = y
        self.neural_network = neural_network
        self.id = id

    def step(self, environment):
        self.neural_network.process(organism=self, environment=environment)

        # Select the ActionNeuron with the highest value
        max_value = -float('inf')
        best_action = None
        for action_neuron in self.neural_network.action_neurons:
            if action_neuron.get_value() > max_value:
                max_value = action_neuron.get_value()
                best_action = action_neuron.get_action()
        
        if best_action:
            best_action.perform(self)

