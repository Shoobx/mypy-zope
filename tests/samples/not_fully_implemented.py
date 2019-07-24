"""A simple valid interface declaration
"""
import zope.interface


class ISomething(zope.interface.Interface):
    def hello(x: int, y: str) -> None:
        pass


@zope.interface.implementer(ISomething)
class Something(object):
    pass


def run(smth: ISomething):
    smth.hello(1, "test")


def main() -> None:
    smth = Something()
    run(smth)


if __name__ == '__main__':
    main()

"""
<output>
not_fully_implemented.py:12: error: 'Something' is missing following 'ISomething' interface members: hello.
</output>
"""
