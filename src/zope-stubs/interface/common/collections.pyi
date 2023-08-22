from _typeshed import Incomplete
from collections import abc
from zope.interface.common import ABCInterface

class IContainer(ABCInterface):
    abc = abc.Container
    def __contains__(other) -> bool: ...

class IHashable(ABCInterface):
    abc = abc.Hashable

class IIterable(ABCInterface):
    abc = abc.Iterable
    def __iter__(): ...

class IIterator(IIterable):
    abc = abc.Iterator

class IReversible(IIterable):
    abc: Incomplete
    def __reversed__() -> None: ...

class IGenerator(IIterator):
    abc: Incomplete

class ISized(ABCInterface):
    abc = abc.Sized

class ICollection(ISized, IIterable, IContainer):
    abc: Incomplete

class ISequence(IReversible, ICollection):
    abc = abc.Sequence
    extra_classes: Incomplete
    ignored_classes: Incomplete
    def __reversed__() -> None: ...
    def __iter__(): ...

class IMutableSequence(ISequence):
    abc = abc.MutableSequence
    extra_classes: Incomplete

class IByteString(ISequence):
    abc: Incomplete

class ISet(ICollection):
    abc = abc.Set

class IMutableSet(ISet):
    abc = abc.MutableSet

class IMapping(ICollection):
    abc = abc.Mapping
    extra_classes: Incomplete
    ignored_classes: Incomplete

class IMutableMapping(IMapping):
    abc = abc.MutableMapping
    extra_classes: Incomplete
    ignored_classes: Incomplete

class IMappingView(ISized):
    abc = abc.MappingView

class IItemsView(IMappingView, ISet):
    abc = abc.ItemsView

class IKeysView(IMappingView, ISet):
    abc = abc.KeysView

class IValuesView(IMappingView, ICollection):
    abc = abc.ValuesView
    def __contains__(other) -> bool: ...

class IAwaitable(ABCInterface):
    abc: Incomplete

class ICoroutine(IAwaitable):
    abc: Incomplete

class IAsyncIterable(ABCInterface):
    abc: Incomplete

class IAsyncIterator(IAsyncIterable):
    abc: Incomplete

class IAsyncGenerator(IAsyncIterator):
    abc: Incomplete
