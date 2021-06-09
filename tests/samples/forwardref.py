"""Method parameters refers to yet undeclared type
"""

import zope.interface

class ISomething(zope.interface.Interface):
    def hello(thing: "IThing") -> None:
        pass

@zope.interface.implementer(ISomething)
class Something(object):
    def hello(self, thing: "IThing") -> None:  # Wrong kind of list
        print(f"Hello, {thing.get_name()}")
        reveal_type(thing)


class IThing(zope.interface.Interface):
    def get_name() -> str:
        pass

"""
<output>
forwardref.py:14: note: Revealed type is "__main__.IThing"
</output>
"""
