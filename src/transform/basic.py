from glitch_operators import Operation

import numpy as np


class Flip(Operation):
    def __init__(self, axis=0):
        self.axis = axis

    def run(self, image):
        return np.flip(image, axis=self.axis)