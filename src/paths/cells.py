import random
import numpy as np
from scipy.misc import imresize


def generate_rule(rule_number):
    rule = {}
    for left in [False, True]:
        for middle in [False, True]:
            for right in [False, True]:
                rule[(left, middle, right)] = rule_number % 2 == 1
                rule_number //= 2
    return rule


def rand_bool():
    return random.random() > 0.5


def generate_ca(rule, size, scale=1):
    height_o, width_o = size
    height, width = height_o // scale, width_o // scale
    ca = np.zeros((height, width))

    ca[0, :] = np.random.rand(width) > 0.5
    for x in range(1, height):
        ca[x, 0] = np.random.rand() > 0.5
        ca[x, -1] = np.random.rand() > 0.5
        for y in range(1, width-1):
            ca[x, y] = rule[(ca[x-1][y-1], ca[x-1][y], ca[x-1][y+1])]

    ca = imresize(ca, [height_o, width_o], 'nearest')
    return ca
