from glitch_operators import Operation, NOP
from transform.basic import Flip

import numpy as np


class Sort(Operation):
    def __init__(self, axis=0, reverse=False):
        self.axis = axis
        if reverse:
            self.flip = Flip(axis=axis)
        else:
            self.flip = NOP()

    def run(self, image):
        result = np.sort(image, axis=self.axis)
        return self.flip.run(result)
