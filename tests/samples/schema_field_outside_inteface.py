import zope.interface
import zope.schema

class Bookmark(object):
    # This field is not used inside an interface. It will be treated as
    # zope.schema.TextLine type
    textline = zope.schema.TextLine(
        title='Title',
        description='Optional text line',
        required=False)


def main() -> None:
    bm = Bookmark()
    bm.textline = "text"  # Error, zope.schema.TextLine is expected

if __name__ == '__main__':
    main()

"""
<output>
schema_field_outside_inteface.py:15: error: Incompatible types in assignment (expression has type "str", variable has type "TextLine")
</output>
"""
