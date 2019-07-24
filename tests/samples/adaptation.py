"""A simple valid interface declaration
"""
import zope.interface


class ISomething(zope.interface.Interface):
    def hello(x: int, y: str) -> None:
        pass

@zope.interface.implementer(ISomething)
class AbstractSomething(object):
    def thefunc(self) -> None:
        pass
    pass

@zope.interface.implementer(ISomething)
class ConcreteSomething(object):
    def hello(self, x: int, y: str) -> None:
        pass

class Context(object):
    pass

def main() -> None:
    ctx = Context()
    smth = ISomething(ctx)
    smth.hello(2, 3)  # Error: second argument is expected to be string

    asmth = AbstractSomething()  # Error, cannot instantiate abstract class

    csmth = ConcreteSomething()  # Can instantiate (using default object constructor)

if __name__ == '__main__':
    main()

"""
<output>
adaptation.py:11: error: 'AbstractSomething' is missing following 'ISomething' interface members: hello.
adaptation.py:27: error: Argument 2 to "hello" of "ISomething" has incompatible type "int"; expected "str"
</output>
"""
