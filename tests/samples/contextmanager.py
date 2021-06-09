from collections import Iterator
from contextlib import contextmanager
from typing import TypeVar, Generic

_T = TypeVar("_T")


class A(Generic[_T]):
    pass

@contextmanager
def m(x: _T) -> Iterator[A[_T]]:
    ...


with m(7) as x:
    reveal_type(x)
    print(x)


"""
<output>
contextmanager.py:17: note: Revealed type is "__main__.A*[builtins.int*]"
</output>
"""
