"""Interfaces can be introspected by a set of methods"""

import zope.interface
import zope.schema
from zope.schema.fieldproperty import FieldProperty

class IBookmark(zope.interface.Interface):
    url = zope.schema.TextLine()


@zope.interface.implementer(IBookmark)
class Bookmark:
    url = FieldProperty(IBookmark['url'])


def main() -> None:
    bm = Bookmark()
    reveal_type(bm.url)
    reveal_type(IBookmark.url)
    bm.url = 'http'


if __name__ == '__main__':
    main()

"""
FieldProperty cannot find out the type of the field, unfortunately, so
types of all FieldProeprties are Any. Maybe this will get fixed some day.

<output>
interface_fieldproperty.py:18: note: Revealed type is "Any"
interface_fieldproperty.py:19: note: Revealed type is "builtins.str"
</output>
"""
