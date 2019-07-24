"""A simple valid interface declaration
"""

import zope.interface


class ISomething(zope.interface.Interface):
    def hello(x: int, y: str) -> None:
        pass


@zope.interface.implementer(ISomething)
class Something(object):
    def hello(self, x: int, y: str) -> None:
        print(f"X: {x}, Y: {y}")


def run(smth: ISomething):
    smth.hello(1, "test")


def main() -> None:
    smth = Something()
    run(smth)


if __name__ == '__main__':
    main()

"""
<output>
</output>
"""
