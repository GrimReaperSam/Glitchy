from scipy.misc import imread, imsave
from src.pixel_sorting.basic import Sort

if __name__ == '__main__':
    image = imread('resources/scene.jpg')
    result = Sort(2, True).run(image)
    imsave('results/result.jpg', result)
