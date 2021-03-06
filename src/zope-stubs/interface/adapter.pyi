# Stubs for zope.interface.adapter (Python 3.6)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional
from zope.interface._zope_interface_coptimizations import LookupBase, VerifyingBase

class BaseAdapterRegistry:
    __bases__: Any = ...
    def __init__(self, bases: Any = ...) -> None: ...
    def changed(self, originally_changed: Any) -> None: ...
    def register(self, required: Any, provided: Any, name: Any, value: Any): ...
    def registered(self, required: Any, provided: Any, name: Any = ...): ...
    def unregister(self, required: Any, provided: Any, name: Any, value: Optional[Any] = ...): ...
    def subscribe(self, required: Any, provided: Any, value: Any) -> None: ...
    def unsubscribe(self, required: Any, provided: Any, value: Optional[Any] = ...): ...
    def get(self, _: Any): ...

class LookupBaseFallback:
    def __init__(self) -> None: ...
    def changed(self, ignored: Optional[Any] = ...) -> None: ...
    def lookup(self, required: Any, provided: Any, name: Any = ..., default: Optional[Any] = ...): ...
    def lookup1(self, required: Any, provided: Any, name: Any = ..., default: Optional[Any] = ...): ...
    def queryAdapter(self, object: Any, provided: Any, name: Any = ..., default: Optional[Any] = ...): ...
    def adapter_hook(self, provided: Any, object: Any, name: Any = ..., default: Optional[Any] = ...): ...
    def lookupAll(self, required: Any, provided: Any): ...
    def subscriptions(self, required: Any, provided: Any): ...
LookupBasePy = LookupBaseFallback
LookupBase = LookupBaseFallback

class VerifyingBaseFallback(LookupBaseFallback):
    def changed(self, originally_changed: Any) -> None: ...
    def lookupAll(self, required: Any, provided: Any): ...
    def subscriptions(self, required: Any, provided: Any): ...
VerifyingBasePy = VerifyingBaseFallback
VerifyingBase = VerifyingBaseFallback

class AdapterLookupBase:
    def __init__(self, registry: Any) -> None: ...
    def changed(self, ignored: Optional[Any] = ...) -> None: ...
    def init_extendors(self) -> None: ...
    def add_extendor(self, provided: Any) -> None: ...
    def remove_extendor(self, provided: Any) -> None: ...
    def queryMultiAdapter(self, objects: Any, provided: Any, name: Any = ..., default: Optional[Any] = ...): ...
    def names(self, required: Any, provided: Any): ...
    def subscribers(self, objects: Any, provided: Any): ...

class AdapterLookup(AdapterLookupBase, LookupBase): ...

class AdapterRegistry(BaseAdapterRegistry):
    LookupClass: Any = ...
    def __init__(self, bases: Any = ...) -> None: ...
    def changed(self, originally_changed: Any) -> None: ...

class VerifyingAdapterLookup(AdapterLookupBase, VerifyingBase): ...

class VerifyingAdapterRegistry(BaseAdapterRegistry):
    LookupClass: Any = ...
