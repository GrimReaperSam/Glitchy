import numpy as np

from glitch_operators import Operation, Chain


class Flip(Operation):
    def __init__(self, axis=0):
        self.axis = axis

    def run(self, image):
        return np.flip(image, axis=self.axis)


class Rot90(Operation):
    def __init__(self, times=1):
        self.times = times

    def run(self, image):
        return np.rot90(image, self.times)


class ApplyRot90(Operation):
    def __init__(self, operation):
        self.operation = Chain(Rot90(times=1), operation, Rot90(times=-1))

    def run(self, image):
        return self.operation.run(image)
