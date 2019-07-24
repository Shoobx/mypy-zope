"""zope.interface provides an abstract attribute for classes

It is translated to Any type.
"""
import zope.interface

class IBookmark(zope.interface.Interface):
    field = zope.interface.Attribute('Arbitrary Attribute')


@zope.interface.implementer(IBookmark)
class Bookmark(object):
    field = None


def main() -> None:
    bm: IBookmark = Bookmark()

    # We can assign anything to abstract attributes
    bm.field = 343
    bm.field = None
    bm.field = "Sample"

if __name__ == '__main__':
    main()

"""
<output>
</output>
"""
