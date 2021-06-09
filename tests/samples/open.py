reveal_type(open('str'))
reveal_type(open('str', 'b'))

"""
<output>
open.py:1: note: Revealed type is "typing.TextIO"
open.py:2: note: Revealed type is "typing.BinaryIO"
</output>
"""
