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
incompatible_signature.py:14: error: Argument 2 of "Something" is incompatible with "hello" of supertype "ISomething"; supertype defines the argument type as "str"
incompatible_signature.py:14: note: This violates the Liskov substitution principle
incompatible_signature.py:14: note: See https://mypy.readthedocs.io/en/stable/common_issues.html#incompatible-overrides
</output>
"""
