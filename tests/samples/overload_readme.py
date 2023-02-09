"""Overload example from README
"""

from typing import Optional, Union, List, overload
import zope.interface


class IAnimal(zope.interface.Interface):
    @overload
    def say() -> str:
        ...

    @overload
    def say(count: int) -> List[str]:
        ...

    def say(count: Optional[int] = None) -> Union[str, List[str]]:
        pass


@zope.interface.implementer(IAnimal)
class Cow(object):
    @overload
    def say(self) -> str:
        ...

    @overload
    def say(self, count: int) -> List[str]:
        ...

    def say(self, count: Optional[int] = None) -> Union[str, List[str]]:
        if count is None:
            return "Mooo"
        return ["Mooo"] * count

"""
<output>
</output>
"""
