import random
import numpy as np

from ..paths import PATHS, KEYS
from glitch_operators import Operation


def evaluate(pixels, sort_fn):
    if sort_fn == 'intensity':
        return pixels.sum(axis=1)
    elif sort_fn == 'maximum':
        return pixels.max(axis=1)
    elif sort_fn == 'minimum':
        return pixels.min(axis=1)
    else:
        return sort_fn(pixels)


class SortInterval(Operation):
    def __init__(self, sort_fn='intensity', interval_size=50):
        self.sort_fn = sort_fn
        self.interval_size = interval_size

    def run(self, image):
        flat = image.reshape((-1, 3))
        start = 0
        end = 0
        while end < flat.size:
            end = min(random.randint(start, start + self.interval_size), flat.size)
            curr_pixels = flat[start:end]
            indices = np.argsort(evaluate(curr_pixels, self.sort_fn))
            flat[start:end] = curr_pixels[indices]
            start = end
        return flat.reshape(image.shape)


class SortPath(Operation):
    def __init__(self, path='horizontal', path_kwargs=None, key='intensity'):
        self.path = PATHS[path]
        self.path_kwargs = path_kwargs if path_kwargs is not None else {}
        self.key = KEYS[key]

    def run(self, image):
        size = image.shape[:2]
        result = np.copy(image)
        path_iterator = self.path(size, **self.path_kwargs)
        keys = self.key(image)

        for row_iter in path_iterator:
            items = np.array(list(row_iter))
            if items.size == 0:
                continue
            subpart = image[items[:, 0], items[:, 1]]
            subpartKey = keys[items[:, 0], items[:, 1]]
            indices = np.argsort(subpartKey)
            result[items[:, 0], items[:, 1]] = subpart[indices, :]

        return result
