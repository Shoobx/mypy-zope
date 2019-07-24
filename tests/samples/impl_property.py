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
Properties are not type-checked in current version, so no error output
<output>
</output>
"""
