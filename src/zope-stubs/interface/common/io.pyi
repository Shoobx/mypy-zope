import io as abc
from _typeshed import Incomplete
from zope.interface.common import ABCInterface as ABCInterface

class IIOBase(ABCInterface):
    abc = abc.IOBase

class IRawIOBase(IIOBase):
    abc = abc.RawIOBase

class IBufferedIOBase(IIOBase):
    abc = abc.BufferedIOBase
    extra_classes: Incomplete

class ITextIOBase(IIOBase):
    abc = abc.TextIOBase
