from typing import Optional, Union, List, overload
from zope.interface import Interface, implementer


class ISomething(Interface):
    @overload
    def getStuff(index: int) -> int:
        ...

    @overload
    def getStuff(index: None = None) -> List[int]:
        ...

    def getStuff(index: Optional[int] = None) -> Union[int, List[int]]:
        """
        A method with an awkwardly typed signature: if called with an
        argument, it returns a result; if called without an argument,
        it returns a list of results.
        """
        ...


@implementer(ISomething)
class MySomething:
    @overload
    def getStuff(self, index: int) -> int:
        ...

    @overload
    def getStuff(self, index: None = None) -> List[int]:
        ...

    def getStuff(self, index: Optional[int] = None) -> Union[int, List[int]]:
        if index is None:
            return [1, 2, 3, 4]
        else:
            return 42


z = MySomething()
i: int = z.getStuff(1)
j: List[int] = z.getStuff()

z2: ISomething = ISomething(z)
i = z.getStuff(1)
j = z.getStuff()

reveal_type(z.getStuff)
reveal_type(z2.getStuff)

"""
<output>
overload.py:48: note: Revealed type is "Overload(def (index: builtins.int) -> builtins.int, def (index: None =) -> builtins.list[builtins.int])"
overload.py:49: note: Revealed type is "Overload(def (index: builtins.int) -> builtins.int, def (index: None =) -> builtins.list[builtins.int])"
</output>
"""
