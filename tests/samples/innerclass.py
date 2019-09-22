"""Dynamic subclassing is handled without errors"""

def decorator(cls):
    class SuperClass(cls):
        pass

"""
<output>
</output>
"""
