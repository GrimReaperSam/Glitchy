from imageio import imread, imwrite
from src.pixel_sorting import *

if __name__ == '__main__':
    image = imread('resources/scene.jpg')

    sort = SortInterval(sort_type='maximum', interval_size=100)
    result = sort.run(image)

    imwrite('results/result.jpg', result)
