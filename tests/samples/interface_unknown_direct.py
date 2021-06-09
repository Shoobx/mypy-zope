"""When interface is imported from unknown package (one without stubs),
do not produce errors. Even if imported directly.
"""

import zope.interface

from unknown.interfaces import IUnknownInterface

@zope.interface.implementer(IUnknownInterface)
class Bookmark(object):
    pass

def main() -> None:
    bm: IUnknownInterface = Bookmark()
    reveal_type(bm)


"""
<output>
interface_unknown_direct.py:7: error: Cannot find implementation or library stub for module named "unknown.interfaces"
interface_unknown_direct.py:7: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
interface_unknown_direct.py:15: note: Revealed type is "Any"
</output>
"""
