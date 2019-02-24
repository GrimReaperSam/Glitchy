import random
import numpy as np

from ..paths import PATHS, KEYS
from glitch_operators import Operation


def get_intervals(total, interval, progressive=0., randomize=False):
    current = 0
    max_interval = interval
    additive_step = max_interval * progressive
    while current < total:
        max_interval += additive_step
        if randomize:
            interval = random.randint(1, int(max_interval) + 1)
        else:
            interval = int(max_interval)
        yield np.s_[current: current + interval]
        current += interval


class SortPath(Operation):
    def __init__(self, path='horizontal', path_kwargs=None, key='intensity',
                 interval=0, progressive=0., randomize=False):
        self.path = PATHS[path]
        self.path_kwargs = path_kwargs if path_kwargs is not None else {}
        self.key = KEYS[key]
        self.interval = interval
        self.progressive = progressive
        self.randomize = randomize

    def run(self, image):
        size = image.shape[:2]
        result = np.copy(image)
        path_iterator = self.path(size, **self.path_kwargs)
        keys = self.key(image)

        for row_iter in path_iterator:
            items = np.array(list(row_iter))
            if items.size == 0:
                continue
            jump = self.interval if self.interval != 0 else items.shape[0]
            intervals = get_intervals(items.shape[0], jump, self.progressive, self.randomize)
            for s in intervals:
                subpart = image[items[s, 0], items[s, 1]]
                subpart_key = keys[items[s, 0], items[s, 1]]

                indices = np.argsort(subpart_key)
                result[items[s, 0], items[s, 1]] = subpart[indices, :]

        return result
