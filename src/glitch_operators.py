import math
import random

import numpy as np


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


class Tile(Operation):
    def __init__(self, operation, size, density=1., randomize=False):
        self.operation = operation
        self.size = size
        self.density = density
        self.randomize = randomize

    def run(self, image):
        result = np.copy(image)
        width, height = image.shape[:2]
        tile_width, tile_height = self.size

        i = 0
        tiles_completed = 0
        for y in range(0, height, tile_height):
            for x in range(0, width, tile_width):
                tiles_completed += 1
                i += 1

                if self.randomize:
                    if random.random() > self.density:
                        continue
                else:
                    if self.density == 0 or i < 1.0 / self.density:
                        continue
                    else:
                        i -= 1.0 / self.density

                tile = np.s_[x:x + tile_width, y:y + tile_height, :]
                result[tile] = self.operation.run(image[tile])
        return result


class Channel(Operation):
    def __init__(self, operation, channels=None, independent=False):
        self.operation = operation
        self.channels = channels if channels is not None else [0, 1, 2]
        self.independent = independent

    def run(self, image):
        result = np.copy(image)
        if isinstance(self.operation, list):
            assert(len(self.operation) == len(self.channels))
            for idx, ch in enumerate(self.channels):
                result[:, :, ch:ch + 1] = self.operation[idx].run(image[:, :, ch:ch + 1])
        else:
            if self.independent:
                for ch in self.channels:
                    result[:, :, ch:ch+1] = self.operation.run(image[:, :, ch:ch+1])
            else:
                result[:, :, self.channels] = self.operation.run(image[:, :, self.channels])
        return result
