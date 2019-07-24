"""zope.interface provides an annotated attribute for classes
"""
import typing
import zope.interface

class IFoo(zope.interface.Interface):
    f_str: typing.Text = zope.interface.Attribute("Text Attr")
    f_str_opt: typing.Optional[typing.Text] = zope.interface.Attribute("Optional Text Attr")
    f_int: int = zope.interface.Attribute("Int Attr")
    f_bar: "IBar" = zope.interface.Attribute("Other Intarface Attr")

class IBar(zope.interface.Interface):
    pass

@zope.interface.implementer(IFoo)
class Foo(object):
    f_str = None
    f_str_opt = None
    f_int = None
    f_bar = None

@zope.interface.implementer(IBar)
class Bar(object):
    pass

def main() -> None:
    foo: IFoo = Foo()
    bar: IBar = Bar()

    foo.f_str = "Sample"
    foo.f_str = 10
    foo.f_str = None
    foo.f_str_opt = None
    foo.f_int = 10
    foo.f_bar = bar

if __name__ == '__main__':
    main()

"""
<output>
interface_annotated_attribute.py:31: error: Incompatible types in assignment (expression has type "int", variable has type "str")
interface_annotated_attribute.py:32: error: Incompatible types in assignment (expression has type "None", variable has type "str")
</output>
"""
