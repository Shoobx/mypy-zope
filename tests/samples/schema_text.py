import zope.interface
import zope.schema


class IBookmark(zope.interface.Interface):
    textline = zope.schema.TextLine(
        title='Title',
        description='Optional text line',
        required=False)
    reqtextline = zope.schema.TextLine(
        title='Title',
        description='Implicitly required text line',)
    expreqtextline = zope.schema.TextLine(
        title='Title',
        description='Explicitly required text line',
        required=True)


@zope.interface.implementer(IBookmark)
class Bookmark(object):
    pass

def main() -> None:
    bm = Bookmark()
    bm.textline = 343  # Error, expected to be string
    bm.reqtextline = None  # Error, it is required
    bm.expreqtextline = None  # Error, it is required

if __name__ == '__main__':
    main()

"""
<output>
schema_text.py:25: error: Incompatible types in assignment (expression has type "int", variable has type "Optional[str]")
schema_text.py:26: error: Incompatible types in assignment (expression has type "None", variable has type "str")
schema_text.py:27: error: Incompatible types in assignment (expression has type "None", variable has type "str")
</output>
"""
