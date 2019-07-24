"""zope.interface.implementer accepts multiple interfaces
"""
import zope.interface

class IBookmark(zope.interface.Interface):
    def remember(url: str) -> None:
        pass

class IActionalble(zope.interface.Interface):
    def follow(times: int):
        pass

@zope.interface.implementer(IBookmark, IActionalble)
class Bookmark(object):
    pass

def main() -> None:
    bm1: IBookmark = Bookmark()
    bm1.remember(None)  # Error, string is expected

    bm2: IActionalble = Bookmark()
    bm2.follow("bad number")  # Error: integer is expected

if __name__ == '__main__':
    main()

"""
<output>
multiple_implementer.py:14: error: 'Bookmark' is missing following 'IBookmark' interface members: remember.
multiple_implementer.py:14: error: 'Bookmark' is missing following 'IActionalble' interface members: follow.
multiple_implementer.py:19: error: Argument 1 to "remember" of "IBookmark" has incompatible type "None"; expected "str"
multiple_implementer.py:22: error: Argument 1 to "follow" of "IActionalble" has incompatible type "str"; expected "int"
</output>
"""
