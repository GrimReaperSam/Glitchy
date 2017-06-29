from src.glitch_operators import Chain
from src.transform.basic import *


def test_flip():
    array = np.array([[1, 2], [3, 4]])
    assert np.all(Flip(axis=0).run(array) == [[3, 4], [1, 2]])
    assert np.all(Flip(axis=1).run(array) == [[2, 1], [4, 3]])
    assert np.all(Chain(Flip(0), Flip(1)).run(array) == [[4, 3], [2, 1]])
    assert np.all(Chain(Flip(1), Flip(0)).run(array) == [[4, 3], [2, 1]])
