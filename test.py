import selfless


@selfless.selfless
class A(object):
    
    def __init__(x):
        self.x = x

    def f():
        return self.x + 1


def test_selfless():
    a = A(1)
    assert a.x   == 1
    assert a.f() == 2
