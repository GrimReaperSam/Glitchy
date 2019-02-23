import numpy as np

from glitch_operators import Operation


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

