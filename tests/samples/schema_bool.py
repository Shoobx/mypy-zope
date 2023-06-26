import zope.interface
import zope.schema


class IBookmark(zope.interface.Interface):
    flag = zope.schema.Bool(required=False)

@zope.interface.implementer(IBookmark)
class Bookmark(object):
    flag = True

def main() -> None:
    bm: IBookmark = Bookmark()
    bm.flag = 343  # Error, expected to be boolean
    bm.flag = None
    bm.flag = True

if __name__ == '__main__':
    main()

"""
<output>
schema_bool.py:14: error: Incompatible types in assignment (expression has type "int", variable has type "bool | None")
</output>
"""
