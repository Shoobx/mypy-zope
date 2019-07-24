"""Method parameters is of parameterized type
"""

from typing import List

import zope.interface

class ISomething(zope.interface.Interface):
    def hello(names: List[str]) -> None:
        pass


@zope.interface.implementer(ISomething)
class Something(object):
    def hello(self, names: List[int]) -> None:  # Wrong kind of list
        print(f"Hello, {names}")


"""
<output>
parameterized_types.py:14: error: Invalid implementation of "ISomething"
parameterized_types.py:15: error: Incompatible implementation of 'ISomething.hello': Got def hello(self, names: List[int]) -> None; expected def hello(self, names: List[str]) -> None
</output>
"""
