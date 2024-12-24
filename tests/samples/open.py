reveal_type(open('str'))
reveal_type(open('str', 'rb'))

"""
<output>
open.py:1: note: Revealed type is "_io.TextIOWrapper[_io._WrappedBuffer]"
open.py:2: note: Revealed type is "_io.BufferedReader"
</output>
"""
