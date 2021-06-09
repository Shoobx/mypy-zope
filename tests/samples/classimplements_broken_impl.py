"""Incorrectly implemented interfaces are reported"""

from zope.interface import implementer
from zope.interface import Interface
from zope.interface import classImplements

from unknown import Foo


class IFoo(Interface):
    def foo() -> int:
        pass


classImplements(Foo, IFoo)


"""
<output>
classimplements_broken_impl.py:7: error: Cannot find implementation or library stub for module named "unknown"
classimplements_broken_impl.py:7: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
classimplements_broken_impl.py:15: error: __main__.Foo is not a class, cannot mark it as a interface implementation
</output>
"""
