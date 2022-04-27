import zope.interface
from typing import Type, TypeVar

T = TypeVar('T', bound='zope.interface.Interface')


class IBookmark(zope.interface.Interface):
    @staticmethod
    def create(url: str) -> 'IBookmark':
        pass

def createOb(iface: Type[T]) -> T:
    if zope.interface.interfaces.IInterface.providedBy(iface):
        pass
    return iface(None)

def main(self) -> None:
    bm = createOb(IBookmark)
    reveal_type(bm)

"""
<output>
interface_meta.py:19: note: Revealed type is "__main__.IBookmark"
</output>
"""