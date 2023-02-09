from contextlib import contextmanager
from typing import Iterator, TypeVar, Generic

_T = TypeVar("_T")


class A(Generic[_T]):
    pass

@contextmanager
def m(x: _T) -> Iterator[A[_T]]:
    return iter([A()])


with m(7) as x:
    reveal_type(x)
    print(x)


"""
<output>
contextmanager.py:16: note: Revealed type is "__main__.A[builtins.int]"
</output>
"""
