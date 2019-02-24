from imageio import imread, imwrite
from src.pixel_sorting import *
from src.glitch_operators import *

if __name__ == '__main__':
    image = imread('resources/scene.jpg')

    sort = SortPath(path='vertical', path_kwargs={}, key='intensity',
                    interval=100, interval_kwargs={'randomize': True})
    result = sort.run(image)

    imwrite('results/result.jpg', result)
