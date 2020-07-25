"""Interfaces can be inherited
"""
import zope.interface


class ISomething(zope.interface.Interface):
    def hello(x: int, y: str) -> None:
        pass

class ISuperSomething(ISomething):
    def greet(msg: str) -> None:
        pass

class ISomethingSomething(ISuperSomething):
    def wink(msg: str) -> None:
        pass

@zope.interface.implementer(ISuperSomething)
class SuperSomething(object):
    def hello(self, x: int, y: str) -> None:
        print(f"X: {x}, Y: {y}")

    def greet(self, msg) -> None:
        print(f"Greetings, {msg}")

@zope.interface.implementer(ISomethingSomething)
class SomethingSomething(SuperSomething):
    def wink(self, msg) -> None:
        print(f"{msg} <wink>")

def run(smth: ISomething):
    smth.hello(1, "test")


def greet(smth: ISuperSomething):
    smth.hello(2, "test 2")
    smth.greet("world")


def main() -> None:
    smth = SuperSomething()
    run(smth)

    smthsmth = SomethingSomething()
    smthsmth.greet("bob")
    smthsmth.wink("susanne")
    smthsmth.hello(1, "dude")

    run(smthsmth)


if __name__ == '__main__':
    main()

"""
<output>
</output>
"""
