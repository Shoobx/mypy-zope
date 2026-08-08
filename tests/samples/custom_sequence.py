"""Override a sequence interface"""

from zope.interface.common import sequence

class ICustomSequence(sequence.IFiniteSequence):
    def iterator(first, count):
        pass

    def size() -> int:
        pass

seq = object()
assert ICustomSequence.providedBy(seq)
reveal_type(seq.size())

"""
<output>
custom_sequence.py:14: note: Revealed type is "builtins.int"
</output>
"""
