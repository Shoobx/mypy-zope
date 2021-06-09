"""Interface can define a __getattr__ method
"""
import zope.interface

class IData(zope.interface.Interface):
    def __getattr__(name: str) -> int:
        pass

def main() -> None:
    data = IData(None)
    reveal_type(data.legs)

"""
<output>
interface_getattr.py:11: note: Revealed type is "builtins.int"
</output>
"""
