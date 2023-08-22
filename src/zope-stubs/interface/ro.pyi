from _typeshed import Incomplete

class InconsistentResolutionOrderWarning(PendingDeprecationWarning): ...

class InconsistentResolutionOrderError(TypeError):
    C: Incomplete
    base_ros: Incomplete
    base_tree_remaining: Incomplete
    def __init__(self, c3, base_tree_remaining) -> None: ...

class _NamedBool(int):
    def __new__(cls, val, name): ...

class _ClassBoolFromEnv:
    def __get__(self, inst, klass): ...

class _StaticMRO:
    had_inconsistency: Incomplete
    leaf: Incomplete
    def __init__(self, C, mro) -> None: ...
    def mro(self): ...

class C3:
    @staticmethod
    def resolver(C, strict, base_mros): ...
    direct_inconsistency: bool
    leaf: Incomplete
    memo: Incomplete
    base_tree: Incomplete
    bases_had_inconsistency: Incomplete
    def __init__(self, C, memo) -> None: ...
    @property
    def had_inconsistency(self): ...
    @property
    def legacy_ro(self): ...
    TRACK_BAD_IRO: Incomplete
    STRICT_IRO: Incomplete
    WARN_BAD_IRO: Incomplete
    LOG_CHANGED_IRO: Incomplete
    USE_LEGACY_IRO: Incomplete
    BAD_IROS: Incomplete
    class _UseLegacyRO(Exception): ...
    def mro(self): ...

class _StrictC3(C3): ...
class _TrackingC3(C3): ...

class _ROComparison:
    class Item:
        prefix: str
        item: Incomplete
        def __init__(self, item) -> None: ...
    class Deleted(Item):
        prefix: str
    class Inserted(Item):
        prefix: str
    Empty = str
    class ReplacedBy:
        prefix: str
        suffix: str
        chunk: Incomplete
        total_count: Incomplete
        def __init__(self, chunk, total_count) -> None: ...
        def __iter__(self): ...
    class Replacing(ReplacedBy):
        prefix: str
        suffix: str
    c3: Incomplete
    c3_ro: Incomplete
    legacy_ro: Incomplete
    def __init__(self, c3, c3_ro, legacy_ro) -> None: ...

def ro(C, strict: Incomplete | None = ..., base_mros: Incomplete | None = ..., log_changed_ro: Incomplete | None = ..., use_legacy_ro: Incomplete | None = ...): ...
