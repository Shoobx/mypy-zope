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
    bm = Bookmark()

    # We can assign anything to abstract attributes
    bm.remember(None)  # Error, string is expected
    bm.follow("bad number")  # Error: integer is expected

if __name__ == '__main__':
    main()

"""
<output>
multiple_implementer.py:18: error: Cannot instantiate abstract class 'Bookmark' with abstract attributes 'follow' and 'remember'
multiple_implementer.py:21: error: Argument 1 to "remember" of "IBookmark" has incompatible type "None"; expected "str"
multiple_implementer.py:22: error: Argument 1 to "follow" of "IActionalble" has incompatible type "str"; expected "int"
</output>
"""
