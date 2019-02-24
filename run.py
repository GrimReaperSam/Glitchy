from imageio import imread, imwrite
from src.pixel_sorting import *
from src.glitch_operators import *


if __name__ == '__main__':
    image = imread('resources/scene.jpg')

    sort = SortPath(path='cells', path_kwargs={'rule_number': 18, 'scale': 1}, key='red',
                    interval=250, interval_kwargs={'randomize': True})
    result = Channel(sort, [1]).run(image)

    imwrite('results/result.jpg', result)
