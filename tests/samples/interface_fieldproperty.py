"""Interfaces can be introspected by a set of methods"""

import zope.interface
from zope.schema.fieldproperty import FieldProperty

class IBookmark(zope.interface.Interface):
    field = zope.interface.Attribute('Arbitrary Attribute')


@zope.interface.implementer(IBookmark)
class Bookmark:
    field = FieldProperty(IBookmark['field'])


def main() -> None:
    bm = Bookmark()
    reveal_type(bm.field)


if __name__ == '__main__':
    main()

"""
FieldProperty cannot find out the type of the field, unfortunately, so
types of all FieldProeprties are Any. Maybe this will get fixed some day.

<output>
interface_fieldproperty.py:17: error: Revealed type is 'Any'
</output>
"""
