class InvalidLayersNumber(Exception):
    def __init__(self, message="The number of layers has to be greater or equal than 1."):
        self.message = message
