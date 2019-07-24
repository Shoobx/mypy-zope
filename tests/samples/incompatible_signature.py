"""Something.hello has a signature, incompatible with interface
"""

import zope.interface


class ISomething(zope.interface.Interface):
    def hello(x: int, y: str) -> None:
        pass


@zope.interface.implementer(ISomething)
class Something(object):
    def hello(self, x: int, y: int) -> None:
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
incompatible_signature.py:13: error: Invalid implementation of "ISomething"
incompatible_signature.py:14: error: Incompatible implementation of 'ISomething.hello': Got def hello(self, x: int, y: int) -> None; expected def hello(self, x: int, y: str) -> None
</output>
"""
