import zope.interface
from zope.interface.common import mapping

class IBookmarkContainer(mapping.IMapping):
    pass

@zope.interface.implementer(IBookmarkContainer)
class BadContainer(object):
    def values(self):
        pass

@zope.interface.implementer(IBookmarkContainer)
class GoodContainer(dict):
    pass


def main() -> None:
    bc: IBookmarkContainer = GoodContainer()
    bc['one'] = 1

if __name__ == '__main__':
    main()

"""
<output>
interface_mapping.py:8: error: 'BadContainer' is missing following 'zope.interface.common.mapping.IItemMapping' interface members: __getitem__.
interface_mapping.py:8: error: 'BadContainer' is missing following 'zope.interface.common.mapping.IReadMapping' interface members: __contains__, get.
interface_mapping.py:8: error: 'BadContainer' is missing following 'zope.interface.common.mapping.IEnumerableMapping' interface members: __iter__, __len__, items, keys.
interface_mapping.py:8: error: 'BadContainer' is missing following 'zope.interface.common.mapping.IWriteMapping' interface members: __delitem__, __setitem__.
</output>
"""
