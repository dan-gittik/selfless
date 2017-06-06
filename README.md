# Selfless

A nifty decorator to get rid of the unnecessary ``self`` parameter in methods.

```python
from selfless import selfless

@selfless
class A:
    
    def __init__(x):
        self.x = x

    def f():
        return self.x + 1

a = A(1)
assert a.x   == 1
assert a.f() == 2
```
