reveal_type(open('str'))
reveal_type(open('str', 'rb'))

"""
<output>
open.py:1: note: Revealed type is "io.TextIOWrapper"
open.py:2: note: Revealed type is "io.BufferedReader"
</output>
"""
