from src.glitch_operators import *


class Double(Operation):
    def run(self, image):
        return image * 2


class Increment(Operation):
    def run(self, image):
        return image + 1


def test_repeat():
    assert Repeat(Double(), 1).run(1) == 2
    assert Repeat(Double(), 4).run(1) == 16
    assert Repeat(Double(), 1).run(3) == 6
    assert Repeat(Increment(), 3).run(15) == 18


def test_chain():
    assert Chain(Double(), Increment(), Double()).run(1) == 6
    assert Chain(Increment(), Double()).run(9) == 20
    assert Repeat(Chain(Increment(), Double()), 2).run(1) == 10

