import random
import numpy as np

from glitch_operators import Operation


def evaluate(pixels, sort_type):
    if sort_type == 'intensity':
        return pixels.sum(axis=1)
    elif sort_type == 'maximum':
        return pixels.max(axis=1)
    elif sort_type == 'minimum':
        return pixels.min(axis=1)
    else:
        pass


class SortInterval(Operation):
    def __init__(self, sort_type='intensity', interval_size=50):
        self.sort_type = sort_type
        self.interval_size = interval_size

    def run(self, image):
        flat = image.reshape((-1, 3))
        start = 0
        end = 0
        while end < flat.size:
            end = min(random.randint(start, start + self.interval_size), flat.size)
            curr_pixels = flat[start:end]
            indices = np.argsort(evaluate(curr_pixels, self.sort_type))
            flat[start:end] = curr_pixels[indices]
            start = end
        return flat.reshape(image.shape)
