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
parameterized_types.py:15: error: Argument 1 of "Something" is incompatible with "hello" of supertype "ISomething"; supertype defines the argument type as "list[str]"
parameterized_types.py:15: note: This violates the Liskov substitution principle
parameterized_types.py:15: note: See https://mypy.readthedocs.io/en/stable/common_issues.html#incompatible-overrides
</output>
"""
