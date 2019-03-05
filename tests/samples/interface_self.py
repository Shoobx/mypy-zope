"""When someone leaves `self` as a parameter in interface function,
bec more helpful in identifying the issue
"""

import zope.interface

class IAnimal(zope.interface.Interface):
    def say(self) -> None:
        pass

@zope.interface.implementer(IAnimal)
class Cow(object):
    def say(self) -> None:
        print("Moooo")

"""
<output>
interface_self.py:8: error: Interface methods should not have 'self' argument
</output>
"""
