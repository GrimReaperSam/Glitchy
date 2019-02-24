from imageio import imread, imwrite
from src.pixel_sorting import *
from src.glitch_operators import *

if __name__ == '__main__':
    image = imread('resources/scene.jpg')

    sort = SortPath(path='random', path_kwargs={}, key='intensity')
    result = Tile(Channel(sort, [0, ], True), (50, 50)).run(image)

    imwrite('results/result.jpg', result)
