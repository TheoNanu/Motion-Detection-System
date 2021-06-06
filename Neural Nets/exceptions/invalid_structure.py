class InvalidNeuralNetStructure(Exception):
    def __init__(self, message="The neural network provided has an invalid structure." +
                               "Make sure the first layer of your network is a dense layer."):
        self.message = message
