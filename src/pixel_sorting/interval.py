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


def rearrange_keys(keys, mirror=False, splice=0, splice_random=False):
    if len(keys) == 0:
        return keys
    new_keys = list(keys)

    if mirror:
        get_index = put_index = 0
        while get_index < len(keys):
            new_keys[put_index] = keys[get_index]
            get_index += 1
            if put_index >= 0:
                put_index += 1
            put_index *= -1

    if splice_random:
        splice_start = random.randrange(len(keys))
    elif splice > 0:
        splice_start = int((len(keys) - 1) * splice)
    else:
        splice_start = None

    if splice_start is not None:
        new_keys = new_keys[splice_start:] + new_keys[:splice_start]

    return new_keys


class SortPath(Operation):
    def __init__(self, path='horizontal', path_kwargs=None,
                 interval=0, interval_kwargs=None, key='intensity', keys_kwargs=None):
        self.path = PATHS[path]
        self.path_kwargs = path_kwargs if path_kwargs is not None else {}

        self.interval = interval
        self.interval_kwargs = interval_kwargs if interval_kwargs is not None else {}

        self.key = KEYS[key]
        self.keys_kwargs = keys_kwargs if keys_kwargs is not None else {}

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
            intervals = get_intervals(items.shape[0], jump, **self.interval_kwargs)
            for s in intervals:
                subpart = image[items[s, 0], items[s, 1]]
                subpart_key = keys[items[s, 0], items[s, 1]]

                subpart_key = rearrange_keys(subpart_key, **self.keys_kwargs)

                indices = np.argsort(subpart_key)
                result[items[s, 0], items[s, 1]] = subpart[indices, :]

        return result
