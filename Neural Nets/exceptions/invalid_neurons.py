class InvalidNeuronsNumber(Exception):
    def __init__(self, message="The number of neurons for a layer has to be greater or equal than 1."):
        self.message = message
