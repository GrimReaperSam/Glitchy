import random

def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0


def is_in_bounds(point, min_b, max_b):
    if point[0] >= max_b[0] or point[0] < min_b[0]:
        return False
    if point[1] >= max_b[1] or point[1] < min_b[1]:
        return False
    return True


def coords_to_index(coords, width):
    return coords[1] * width + coords[0]


def weighted_random_choice(items):
    l = list(items)
    r = random.random() * sum([i[1] for i in l])
    for x, p in l:
        if p > r:
            return x
        r -= p
    return None
