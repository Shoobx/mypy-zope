"""zope.interface provides an abstract attribute for classes

It is translated to Any type.
"""
import zope.interface
from typing import Optional

class IBookmark(zope.interface.Interface):
    field = zope.interface.Attribute('Arbitrary Attribute')


@zope.interface.implementer(IBookmark)
class Bookmark(object):
    field = None

def main(obj: Optional[IBookmark]) -> None:

    if not IBookmark.providedBy(obj):
        reveal_type(obj)
    else:
        reveal_type(obj)
    reveal_type(obj)

    cls = obj.__class__
    if IBookmark.implementedBy(cls):
        reveal_type(cls)
    else:
        reveal_type(cls)
    reveal_type(cls)

if __name__ == '__main__':
    main(Bookmark())

"""
<output>
interface_implications.py:19: note: Revealed type is "None"
interface_implications.py:21: note: Revealed type is "__main__.IBookmark"
interface_implications.py:22: note: Revealed type is "Union[__main__.IBookmark, None]"
interface_implications.py:26: note: Revealed type is "Type[__main__.IBookmark]"
interface_implications.py:28: note: Revealed type is "Type[None]"
interface_implications.py:29: note: Revealed type is "Union[Type[__main__.IBookmark], Type[None]]"
 </output>
"""
