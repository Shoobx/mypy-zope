from zope.interface import implementer
from zope.interface import Interface
from zope.interface import classImplements


class IFoo(Interface):
    def foo() -> int:
        pass


class IBar(Interface):
    def bar() -> str:
        pass


class FooBar:
    def foo(self) -> int:
        return 0

    def bar(self) -> str:
        return ""


classImplements(FooBar, IFoo, IBar)


foo: IFoo = FooBar()
bar: IBar = FooBar()


"""
<output>
</output>
"""
