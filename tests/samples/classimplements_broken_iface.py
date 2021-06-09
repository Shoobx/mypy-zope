"""Incorrectly implemented interfaces are reported"""

from zope.interface import implementer
from zope.interface import Interface
from zope.interface import classImplements

from unknown import IFoo


def ImNotAnInterface() -> int:
    return 0

ImNotAnInterfaceEither = "indeed"

class Foo:
    def foo(self) -> int:
        return 0

classImplements(Foo, IFoo, ImNotAnInterface, ImNotAnInterfaceEither, 2+2)


"""
<output>
classimplements_broken_iface.py:7: error: Cannot find implementation or library stub for module named "unknown"
classimplements_broken_iface.py:7: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
classimplements_broken_iface.py:19: error: __main__.IFoo is not a class, cannot mark __main__.Foo as an implementation of __main__.IFoo
classimplements_broken_iface.py:19: error: __main__.ImNotAnInterface is not an interface
classimplements_broken_iface.py:19: error: Make sure you have stubs for all packages that provide interfaces for __main__.ImNotAnInterface class hierarchy.
classimplements_broken_iface.py:19: error: __main__.ImNotAnInterfaceEither is not a class, cannot mark __main__.Foo as an implementation of __main__.ImNotAnInterfaceEither
classimplements_broken_iface.py:19: error: expression is not a class, cannot mark __main__.Foo as an implementation of expression
</output>
"""
