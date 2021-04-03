"""Incorrectly implemented interfaces are reported"""

from zope.interface import implementer
from zope.interface import Interface
from zope.interface import classImplements


class IFoo(Interface):
    def foo() -> int:
        pass


class Foo:
    def bar(self) -> int:
        return 0


classImplements(Foo, IFoo)


foo: IFoo = Foo()


"""
<output>
classimplements_wrong.py:18: error: 'Foo' is missing following 'IFoo' interface members: foo.
</output>
"""
