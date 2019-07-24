"""Interface implements attribute as property
"""
import zope.interface


class IBookmark(zope.interface.Interface):
    number: int
    text: str

@zope.interface.implementer(IBookmark)
class Bookmark(object):
    @property
    def number(self) -> str:
        return "hello"

    @number.setter
    def number(self, value: str) -> None:
        pass

    @property
    def text(self) -> int:
        return 5


def main() -> None:
    bm: IBookmark = Bookmark()
    bm.number = 12

"""
<output>
impl_property.py:11: error: Invalid implementation of "IBookmark"
impl_property.py:13: error: Incompatible implementation of 'IBookmark.number': Got "str"; expected "int"
impl_property.py:21: error: Incompatible implementation of 'IBookmark.text': Got "int"; expected "str"
</output>
"""
