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
<output>
</output>
"""
