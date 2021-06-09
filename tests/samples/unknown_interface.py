"""When importing an interface from unknown module, we just ignore it
"""
import zope.interface

from unknown import IUnknownInterface

@zope.interface.implementer(IUnknownInterface)
class Bookmark(object):
    flag = True

def main() -> None:
    bm = Bookmark()
    bm.flag = False

if __name__ == '__main__':
    main()

"""
<output>
unknown_interface.py:5: error: Cannot find implementation or library stub for module named "unknown"
unknown_interface.py:5: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
</output>
"""
