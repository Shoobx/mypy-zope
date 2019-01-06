import zope.interface
import zope.schema

class UnknownField(zope.schema.Field):
    """Field is unknown to mypy-test plugin"""


class IBookmark(zope.interface.Interface):
    field = UnknownField(
        title='Unknown',
        required=False)


@zope.interface.implementer(IBookmark)
class Bookmark(object):
    pass

def main() -> None:
    bm = Bookmark()

    # We can assign anything to unknown fields
    bm.field = 343
    bm.field = None
    bm.field = "Sample"

if __name__ == '__main__':
    main()

"""
<output>
</output>
"""