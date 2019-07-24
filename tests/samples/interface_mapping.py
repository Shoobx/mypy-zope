import zope.interface
from zope.interface.common import mapping

class IBookmarkContainer(mapping.IMapping):
    pass

@zope.interface.implementer(IBookmarkContainer)
class BookmarkContainer(object):
    def values(self):
        pass

def main() -> None:
    bc: IBookmarkContainer = BookmarkContainer()
    bc['one'] = 1

if __name__ == '__main__':
    main()

"""
<output>
interface_mapping.py:8: error: 'BookmarkContainer' is missing following 'IBookmarkContainer' interface members: __contains__, __delitem__, __getitem__, __iter__, __len__, __setitem__, get, items, keys.
</output>
"""
