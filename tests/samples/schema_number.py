import zope.interface
import zope.schema


class IBookmark(zope.interface.Interface):
    cmpl = zope.schema.Complex(required=False)
    real = zope.schema.Real(required=False)
    integer = zope.schema.Int(required=False)


@zope.interface.implementer(IBookmark)
class Bookmark(object):
    cmpl = None
    real = None
    integer = None


def main() -> None:
    bm: IBookmark = Bookmark()
    bm.cmpl = "str"  # Error: number is expected
    bm.cmpl = complex(1, 2)
    bm.cmpl = 1.2
    bm.cmpl = 343
    bm.real = complex(1, 2)  # Error: real is expected
    bm.real = 1.2
    bm.real = 343
    bm.integer = complex(1, 2)  # Error: integer is expected
    bm.integer = 1.2  # Error: integer is expected
    bm.integer = 343


if __name__ == '__main__':
    main()

"""
<output>
schema_number.py:20: error: Incompatible types in assignment (expression has type "str", variable has type "complex | None")
schema_number.py:24: error: Incompatible types in assignment (expression has type "complex", variable has type "float | None")
schema_number.py:27: error: Incompatible types in assignment (expression has type "complex", variable has type "int | None")
schema_number.py:28: error: Incompatible types in assignment (expression has type "float", variable has type "int | None")
</output>
"""
