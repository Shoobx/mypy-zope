"""When metaclass is not defined, ignore it"""

from i.dont.exist import MetaKlass


class Leg(metaclass=MetaKlass):
    pass


"""
<output>
unknown_metaclass.py:3: error: Cannot find implementation or library stub for module named "i.dont.exist"
unknown_metaclass.py:3: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
</output>
"""
