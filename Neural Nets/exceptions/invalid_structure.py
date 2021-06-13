class InvalidNeuralNetStructure(Exception):
    def __init__(self, message="The neural network provided has an invalid structure."):
        self.message = message
