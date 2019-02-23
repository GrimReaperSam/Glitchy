from skimage.color import rgb2lab, lab2lch, rgb2hsv
import random


def red(pixel):
    return pixel[:, :, 0]


def green(pixel):
    return pixel[:, :, 1]


def blue(pixel):
    return pixel[:, :, 2]


def intensity(pixel):
    return pixel.sum(axis=2)


def maximum(pixel):
    return pixel.max(axis=2)


def minimum(pixel):
    return pixel.min(axis=2)


def luma(pixel):
    return 0.2126 * pixel[:, :, 0] + 0.7152 * pixel[:, :, 1] + 0.0722 * pixel[:, :, 2]


def lightness(pixel):
    return lab2lch(rgb2lab(pixel))[:, :,  0]


def chroma(pixel):
    return lab2lch(rgb2lab(pixel))[:, :,  1]


def hue(pixel):
    return lab2lch(rgb2lab(pixel))[:, :,  2]


def saturation(pixel):
    return rgb2hsv(pixel(pixel))[:, :,  1]


def randomly(pixel):
    return random.random()
