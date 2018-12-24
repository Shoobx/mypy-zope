"""Interface contains a method without arguments.

Mypy should not complain.
"""
import zope.interface


class ISomething(zope.interface.Interface):
    def hello() -> None:
        pass


@zope.interface.implementer(ISomething)
class Something(object):
    def hello(self) -> None:
        print("Hello world!")


def run(smth: ISomething):
    smth.hello()


def main() -> None:
    smth = Something()
    run(smth)


if __name__ == '__main__':
    main()

"""
This error should not really be reported, but mypy fix is needed

<output>
no_arg_method.py:9: error: Method must have at least one argument
</output>
"""
