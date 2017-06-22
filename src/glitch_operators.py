class Operation:
    def run(self, image):
        pass


class NOP(Operation):
    def run(self, image):
        return image


class Repeat(Operation):
    def __init__(self, operation, times):
        self.operation = operation
        self.times = times

    def run(self, image):
        result = image
        for i in range(self.times):
            result = self.operation.run(result)
        return result


class Chain(Operation):
    def __init__(self, *operations):
        self.operations = operations

    def run(self, image):
        result = image
        for operation in self.operations:
            result = operation.run(result)
        return result
