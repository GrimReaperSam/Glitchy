from imageio import imread, imwrite
from src.pixel_sorting import *
from src.transform import *

if __name__ == '__main__':
    image = imread('resources/scene.jpg')

    sort = SortPath(path='circles', path_kwargs={})
    result = ApplyRot90(sort).run(image)

    imwrite('results/result.jpg', result)
