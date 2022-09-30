"""
Reproduces a bug where MROs were incorrectly computed for implementers
    https://github.com/Shoobx/mypy-zope/issues/34
    https://github.com/Shoobx/mypy-zope/issues/76
"""

from zope.interface import implementer, Interface


class IProtocol(Interface):
    pass


def main() -> None:
    class Factory:
        # It seems important for "Protocol" to show up as an attribute annotation to
        # trigger the bug(!?)
        protocol: "Protocol"

    @implementer(IProtocol)
    class Protocol:
        pass


if __name__ == '__main__':
    main()

"""
Expect no errors. A specific test checks that we correct compute the MRO of `Protocol`.
<output>
</output>
"""
