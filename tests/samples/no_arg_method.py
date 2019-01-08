"""Interface contains a method without arguments.

Mypy should not complain.
"""
import zope.interface


class ISomething(zope.interface.Interface):
    def hello() -> None:
        pass

    def add(a, b) -> int:
        pass


@zope.interface.implementer(ISomething)
class Something(object):
    def hello(self) -> None:
        print("Hello world!")

    def add(self, a, b):
        return a + b


def run(smth: ISomething):
    smth.hello()
    smth.add(2, 4)


def main() -> None:
    smth = Something()
    run(smth)


if __name__ == '__main__':
    main()

"""
These errors should not really be reported, but mypy fix is needed

<output>
no_arg_method.py:9: error: Method must have at least one argument
no_arg_method.py:27: error: Argument 1 to "add" of "ISomething" has incompatible type "int"; expected "ISomething"
</output>
"""
