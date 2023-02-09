"""When interface is imported from unknown package, but is inherited by other,
we cannot recognize it as an interface. So standard mypy rules apply, with
all the extra error messages.
"""

import zope.interface

from unknown.interfaces import IUnknownInterface

class IKnownInterface(IUnknownInterface):
    def hello():
        pass

@zope.interface.implementer(IKnownInterface)
class Bookmark(object):
    pass


"""
<output>
interface_unknown_inherit.py:8: error: Cannot find implementation or library stub for module named "unknown.interfaces"
interface_unknown_inherit.py:8: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
interface_unknown_inherit.py:11: error: Method must have at least one argument. Did you forget the "self" argument?
interface_unknown_inherit.py:14: error: zope.interface.implementer accepts interface, not __main__.IKnownInterface.
interface_unknown_inherit.py:14: error: Make sure you have stubs for all packages that provide interfaces for __main__.IKnownInterface class hierarchy.
</output>
"""
