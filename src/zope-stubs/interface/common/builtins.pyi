from _typeshed import Incomplete
from zope.interface.common import collections, io, numbers

class IList(collections.IMutableSequence):
    extra_classes: Incomplete
    def sort(key: Incomplete | None = ..., reverse: bool = ...) -> None: ...

class ITuple(collections.ISequence):
    extra_classes: Incomplete

class ITextString(collections.ISequence):
    extra_classes: Incomplete

class IByteString(collections.IByteString):
    extra_classes: Incomplete

class INativeString(ITextString): ...

class IBool(numbers.IIntegral):
    extra_classes: Incomplete

class IDict(collections.IMutableMapping):
    extra_classes: Incomplete

class IFile(io.IIOBase):
    extra_classes: Incomplete
