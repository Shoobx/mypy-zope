"""When interface is imported from unknown package (one without stubs),
do not produce errors.
"""

import zope.interface

from unknown import interfaces

@zope.interface.implementer(interfaces.IUnknownInterface)
class Bookmark(object):
    pass

def main() -> None:
    bm: interfaces.IUnknownInterface = Bookmark()
    reveal_type(bm)


"""
<output>
interface_unknown.py:7: error: Cannot find implementation or library stub for module named "unknown"
interface_unknown.py:7: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
interface_unknown.py:15: note: Revealed type is "Any"
</output>
"""
