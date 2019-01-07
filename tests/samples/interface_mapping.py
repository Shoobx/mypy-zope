import zope.interface
from zope.interface.common import mapping

class IBookmarkContainer(mapping.IMapping):
    pass

@zope.interface.implementer(IBookmarkContainer)
class BookmarkContainer(object):
    def values(self):
        pass

def main() -> None:
    bc = BookmarkContainer()
    bc['one'] = 1

if __name__ == '__main__':
    main()

"""
<output>
interface_mapping.py:13: error: Cannot instantiate abstract class 'BookmarkContainer' with abstract attributes '__contains__', '__delitem__', ... and 'keys' (6 methods suppressed)
</output>
"""
