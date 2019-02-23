import numpy as np

from glitch_operators import Operation


class Sort(Operation):
    def __init__(self, axis=0):
        self.axis = axis

    def run(self, image):
        return np.sort(image, axis=self.axis)


class SortRgbSum(Operation):
    def __init__(self, axis=None, channels=None):
        self.axis = axis
        if channels is None:
            channels = [0, 1, 2]
        self.channels = channels

    def run(self, image):
        flat = np.reshape(image, (-1, 1, image.shape[2])).squeeze()
        avg_img = np.sum(image[:, :, self.channels], axis=2)
        if self.axis:
            indices = np.argsort(avg_img, axis=self.axis)
            if self.axis == 0:
                result = image[indices, np.arange(image.shape[1])[None, :], :]
            else:
                result = image[np.arange(image.shape[0])[:, None], indices, :]
        else:
            avg_img = avg_img.flatten()
            indices = np.argsort(avg_img)
            result = flat[indices].reshape(image.shape)
        return result
