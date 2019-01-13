"""It is not always possible to consistently inject complicated
interface hierarchy into implementation MRO. We warn about such occurances.

By itself, both interface hierarchy and implementation hierarchies are
consistent, but combining them is impossible - resulting inheritance graph
become unsortable.
"""
import zope.interface

class ICreature(zope.interface.Interface): pass
class ISwimmable(zope.interface.Interface): pass
class IReptilia(ICreature): pass
class ICrocodile(ICreature, ISwimmable): pass

@zope.interface.implementer(ISwimmable)
class Swimmable: pass
@zope.interface.implementer(IReptilia)
class Reptilia(Swimmable): pass
@zope.interface.implementer(ICrocodile)
class Crocodile(Reptilia): pass


def main() -> None:
    croc = Crocodile()
    print(croc)

if __name__ == '__main__':
    main()

"""
<output>
bad_mro.py:19: error: Unable to calculate a consistent MRO: cannot merge class hierarchies:
bad_mro.py:19: error:   -> ['__main__.Crocodile', '__main__.Reptilia', '__main__.Swimmable', 'builtins.object', '__main__.ISwimmable', '__main__.IReptilia', '__main__.ICreature', 'zope.interface.interface.Interface']
bad_mro.py:19: error:   -> ['__main__.ICrocodile', '__main__.ICreature', '__main__.ISwimmable', 'zope.interface.interface.Interface']
</output>
"""
