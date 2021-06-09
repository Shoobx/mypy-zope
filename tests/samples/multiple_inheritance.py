"""A simple valid interface declaration
"""
import zope.interface


class IAwesome(zope.interface.Interface):
    def sparkle(count: int) -> None: pass

class IClothing(zope.interface.Interface):
    def wear() -> None: pass

@zope.interface.implementer(IAwesome)
class Awesome:
    def sparkle(self, count: int) -> None: pass

@zope.interface.implementer(IClothing)
class Boots:
    def __init__(self, color: str) -> None: pass
    def wear(self): pass

class AwesomeBoots(Awesome, Boots):
    pass

def main() -> None:
    myboots = AwesomeBoots(color='red')
    myboots.wear()
    myboots.sparkle(5)
    reveal_type(AwesomeBoots.__init__)

if __name__ == '__main__':
    main()

"""
<output>
multiple_inheritance.py:28: note: Revealed type is "def (self: __main__.Boots, color: builtins.str)"
</output>
"""
