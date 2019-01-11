import os
import sys
from typing import List, Dict, Any, Callable, Optional
from typing import Type as PyType
from typing import cast

from mypy.types import (
    Type, Instance, CallableType, UnionType, NoneTyp, AnyType, TypeOfAny
)
from mypy.checker import TypeChecker, is_false_literal
from mypy.nodes import TypeInfo
from mypy.plugin import (
    CheckerPluginInterface, SemanticAnalyzerPluginInterface,
    MethodSigContext, Plugin,
    AnalyzeTypeContext, FunctionContext, MethodContext, AttributeContext,
    ClassDefContext, SymbolTableNode
)
from mypy.semanal import SemanticAnalyzerPass2, merge
from mypy.options import Options

from mypy.nodes import (
    Decorator, Var, Argument, FuncDef, CallExpr, RefExpr, Expression,
    ClassDef, Statement, Block,
    MDEF, ARG_POS, ARG_OPT
)

ZOPE_FIELD_DEFAULT_PARAM_NUM = 3


def _make_optional(required_arg: List[Expression], typ: Type) -> Type:
    # Optionally make type optional
    if not required_arg:
        # Required arg is not provided, assume True
        return typ
    # Check if required_arg represents 'False' (it is "True" by default)
    if not is_false_literal(required_arg[0]):
        return typ

    # Field is explicitly marked as non-required, make it "Optional"
    nonetyp = NoneTyp()
    uniontyp = UnionType([typ, nonetyp])
    return uniontyp


def make_simple_type(fieldtype: str, args: List[List[Expression]],
                     api: CheckerPluginInterface) -> Optional[Type]:
    typename = SIMPLE_FIELD_TO_TYPE.get(fieldtype)
    if not typename:
        return None
    stdtype = api.named_generic_type(typename, [])
    if len(args) -1 < ZOPE_FIELD_DEFAULT_PARAM_NUM:
        return stdtype
    return _make_optional(args[ZOPE_FIELD_DEFAULT_PARAM_NUM], stdtype)


FIELD_TO_TYPE_MAKER = {
    'zope.schema.Text': make_simple_type,
    'zope.schema.Bool': make_simple_type,
    'zope.schema.Complex': make_simple_type,
    'zope.schema.Real': make_simple_type,
    'zope.schema.Int': make_simple_type,

}

SIMPLE_FIELD_TO_TYPE = {
    'zope.schema.Text': 'str',
    'zope.schema.Bool': 'bool',
    'zope.schema.Complex': 'complex',
    'zope.schema.Real': 'float',
    'zope.schema.Int': 'int',
}


class ZopeInterfacePlugin(Plugin):
    def __init__(self, options: Options) -> None:
        here = os.path.dirname(__file__)
        options.mypy_path.append(os.path.join(here, 'stubs'))
        super(ZopeInterfacePlugin, self).__init__(options)

    def log(self, msg: str) -> None:
        if self.options.verbosity  >=1:
            print("ZOPE:", msg, file=sys.stderr)

    def get_type_analyze_hook(self, fullname: str
                              ) -> Optional[Callable[[AnalyzeTypeContext], Type]]:
        # print(f"get_type_analyze_hook: {fullname}")
        return None

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        # print(f"get_function_hook: {fullname}")
        def analyze(function_ctx: FunctionContext) -> Type:
            # strtype = function_ctx.api.named_generic_type('builtins.str', [])
            # optstr = function_ctx.api.named_generic_type('typing.Optional', [strtype])
            api = function_ctx.api
            deftype = function_ctx.default_return_type

            # If we are not processing an interface, leave the type as is
            assert isinstance(api, TypeChecker)
            scopecls = api.scope.active_class()
            if scopecls is None:
                return deftype

            if not self._is_interface(scopecls):
                return deftype

            # If default type is a zope.schema.Field, we should convert it to a
            # python type
            if not isinstance(deftype, Instance):
                return deftype

            parent_names = [t.fullname() for t in deftype.type.mro]
            if 'zope.interface.Attribute' not in parent_names:
                return deftype

            # If it is a konwn field, build a python type out of it
            for clsname in parent_names:
                maker = FIELD_TO_TYPE_MAKER.get(clsname)
                if maker is None:
                    continue

                convtype = maker(clsname, function_ctx.args, function_ctx.api)
                if convtype:
                    self.log(f"Converting a field {deftype} into type {convtype} "
                             f"for {scopecls.fullname()}")
                    return convtype

            # For unknown fields, just return ANY
            self.log(f"Unknown field {deftype} in interface {scopecls.fullname()}")
            return AnyType(TypeOfAny.implementation_artifact,
                           line=deftype.line, column=deftype.column)

        return analyze

    def get_method_signature_hook(self, fullname: str
                                  ) -> Optional[Callable[[MethodSigContext], CallableType]]:
        # print(f"get_method_signature_hook: {fullname}")
        return None

    def get_method_hook(self, fullname: str
                        ) -> Optional[Callable[[MethodContext], Type]]:
        # print(f"get_method_hook: {fullname}")
        return None

    def get_attribute_hook(self, fullname: str
                           ) -> Optional[Callable[[AttributeContext], Type]]:
        # print(f"get_attribute_hook: {fullname}")
        return None

    def get_class_decorator_hook(self, fullname: str
                                 ) -> Optional[Callable[[ClassDefContext], None]]:
        # print(f"get_class_decorator_hook: {fullname}")

        def apply_interface(iface_arg: Expression, class_info: TypeInfo,
                            api: SemanticAnalyzerPluginInterface) -> None:
            if not isinstance(iface_arg, RefExpr):
                api.fail("Argument to implementer should be a ref expression",
                         iface_arg)
                return
            iface_name = iface_arg.fullname
            if iface_name is None:
                api.fail("Interface should be specified (should never happen)", iface_arg)
                return

            iface_type = iface_arg.node
            if iface_type is None:
                return
            if not isinstance(iface_type, TypeInfo):
                # Possibly an interface from unimported package, ignore
                return

            if not self._is_interface(iface_type):
                api.fail(f"zope.interface.implementer accepts interface (not {iface_name})", iface_arg)
                return

            # print("CLASS INFO", class_info)
            md = self._get_metadata(class_info)
            if 'implements' not in md:
                md['implements'] = []
            # impl_list = cast(List[str], md['implements'])
            md['implements'].append(iface_type.fullname())
            self.log(f"Found implementation of {iface_type.fullname()}: {class_info.fullname()}")
            class_info.mro.append(iface_type)

        def analyze(classdef_ctx: ClassDefContext) -> None:
            api = classdef_ctx.api

            decor = cast(CallExpr, classdef_ctx.reason)

            for iface_arg in decor.args:
                apply_interface(iface_arg, classdef_ctx.cls.info, api)

        if fullname=='zope.interface.implementer':
            return analyze
        return None

    def get_metaclass_hook(self, fullname: str
                           ) -> Optional[Callable[[ClassDefContext], None]]:
        # print(f"get_metaclass_hook: {fullname}")
        return None

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        # print(f"get_base_class_hook: {fullname}")
        def analyze_direct(classdef_ctx: ClassDefContext) -> None:
            self.log(f"Found zope interface: {classdef_ctx.cls.fullname}")
            md = self._get_metadata(classdef_ctx.cls.info)
            md['is_interface'] = True

        def analyze_subinterface(classdef_ctx: ClassDefContext) -> None:
            # If one of the bases is an interface, this is also an interface
            if not isinstance(classdef_ctx.reason, RefExpr):
                return
            cls_info = classdef_ctx.cls.info
            api = classdef_ctx.api
            base_name = classdef_ctx.reason.fullname
            if not base_name:
                return
            base_node = api.lookup_fully_qualified_or_none(base_name)
            if not base_node:
                return
            if not isinstance(base_node.node, TypeInfo):
                return

            if self._is_interface(base_node.node):
                self.log(f"Found zope subinterface: {cls_info.fullname()}")
                cls_md = self._get_metadata(cls_info)
                cls_md['is_interface'] = True

        if fullname == 'zope.interface.Interface':
            return analyze_direct

        return analyze_subinterface

    def get_customize_class_mro_hook(self, fullname: str
                                     ) -> Optional[Callable[[ClassDefContext], None]]:
        # print(f"get_customize_class_mro_hook: {fullname}")

        def analyze_interface_base(classdef_ctx: ClassDefContext) -> None:
            # Create fake constructor to mimic adaptation signature
            info = classdef_ctx.cls.info
            api = classdef_ctx.api
            if '__init__' in info.names:
                # already patched
                return

            # Create a method:
            #
            # def __init__(self, obj, alternate=None) -> None
            #
            # This will make interfaces
            selftp = Instance(info, [])
            anytp = AnyType(TypeOfAny.implementation_artifact)
            init_fn = CallableType(
                arg_types=[selftp, anytp, anytp],
                arg_kinds=[ARG_POS, ARG_POS, ARG_OPT],
                arg_names=['self', 'obj', 'alternate'],
                ret_type=NoneTyp(),
                fallback=api.named_type('function')
            )
            newinit = FuncDef('__init__', [], Block([]), init_fn)
            newinit.info = info
            info.names['__init__'] = SymbolTableNode(
                MDEF, newinit, plugin_generated=True)


        def analyze(classdef_ctx: ClassDefContext) -> None:
            info = classdef_ctx.cls.info

            # If we are dealing with an interface, massage it a bit, e.g.
            # inject `self` argument to all methods
            directiface = 'zope.interface.Interface' in [b.type.fullname() for b in info.bases]
            subinterface = any(self._is_interface(b.type) for b in info.bases)
            if directiface or subinterface:
                self._analyze_zope_interface(classdef_ctx.cls)
                return

            # Are we customizing interface implementation instead?
            md = self._get_metadata(info)
            iface_exprs = cast(List[str], md.get('implements'))
            if iface_exprs:
                self._analyze_implementation(classdef_ctx.cls, iface_exprs, classdef_ctx.api)
                return

        if fullname == 'zope.interface.Interface':
            return analyze_interface_base

        return analyze

    def _analyze_implementation(self, cls: ClassDef, iface_exprs: List[str],
                                api: SemanticAnalyzerPluginInterface) -> None:
        info = cls.info
        # Find a suitable __init__ method
        init_method = info.get_method('__init__')
        assert init_method is not None
        if init_method.info.fullname() == 'builtins.object':
            # No __init__ defined for class or its base classes. We are going
            # to insert interface class hierarchies into MRO, which will
            # introduce "adaptation" __init__ method. We need to preserve the
            # ability to instantiate implementation without parameters.
            assert init_method.type is not None
            assert isinstance(init_method.type, CallableType)
            newinit_type = init_method.type \
                .copy_modified(arg_types=[Instance(info, [])]) \
                .with_name(f"{init_method.name()} of {info.name()}")
            # Horrible hack to prevent abstract method instantiation error
            newinit = FuncDef(init_method.name(), [], Block([]), newinit_type)
            newinit.info = info
            info.names['__init__'] = SymbolTableNode(MDEF, newinit,
                                                     plugin_generated=True)

        # Make inteface a superclass of implementation
        seqs = [info.mro]
        for iface_expr in iface_exprs:
            stn = api.lookup_fully_qualified_or_none(iface_expr)
            if stn is None:
                continue
            self.log(f"Adding {iface_expr} to MRO of {info.fullname()}")
            seqs.append(cast(TypeInfo, stn.node).mro)

        info.mro = merge(seqs)

        # XXX: Reuse abstract status checker from SemanticAnalyzerPass2.
        # Ideally, implement a dedicated interface verifier.
        api = cast(SemanticAnalyzerPass2, api)
        api.calculate_abstract_status(info)

    def _analyze_zope_interface(self, cls: ClassDef) -> None:
        self.log(f"Adjusting zope interface: {cls.info.fullname()}")

        for idx, item in enumerate(cls.defs.body):
            if not isinstance(item, FuncDef):
                continue

            replacement = self._adjust_interface_function(cls.info, item)
            cls.defs.body[idx] = replacement

        # Even though interface is abstract, we mark it as non-abstract to
        # allow adaptation pattern: IInterface(context)
        cls.info.is_abstract = False

    def _get_metadata(self, typeinfo: TypeInfo) -> Dict[str, Any]:
        if 'zope' not in typeinfo.metadata:
            typeinfo.metadata['zope'] = {}
        return typeinfo.metadata['zope']

    def _is_interface(self, typeinfo: TypeInfo) -> bool:
        md = self._get_metadata(typeinfo)
        return md.get('is_interface', False)

    def _adjust_interface_function(self, class_info: TypeInfo,
                                   func_def: FuncDef) -> Statement:
        selftype = Instance(class_info, [],
                            line=class_info.line,
                            column=class_info.column)
        selfarg = Argument(Var('self', None), selftype, None, ARG_POS)

        if isinstance(func_def.type, CallableType):
            func_def.type.arg_names.insert(0, 'self')
            func_def.type.arg_kinds.insert(0, ARG_POS)
            func_def.type.arg_types.insert(0, selftype)
        func_def.arg_names.insert(0, 'self')
        func_def.arg_kinds.insert(0, ARG_POS)
        func_def.arguments.insert(0, selfarg)

        func_def.is_abstract = True
        func_def.is_decorated = True
        var = Var(func_def.name(), func_def.type)
        var.is_initialized_in_class=True
        var.info = func_def.info
        var.set_line(func_def.line)
        decor = Decorator(func_def, [], var)
        return decor


# HACK: we want to inject zope stub path into mypy search path. Unfortunately
# there is no legal way for plugins to do that ATM, so we resort to
# monkeypatching.
from mypy import build
from mypy.modulefinder import SearchPaths
class MypyZopeBuildManager(build.BuildManager):
    def __init__(self, data_dir: str, search_paths: SearchPaths, *args: Any, **kwargs: Any) -> None:
        here = os.path.dirname(__file__)
        zope_search_paths = SearchPaths(
            python_path=search_paths.python_path,
            mypy_path=search_paths.mypy_path,
            package_path=search_paths.package_path,
            typeshed_path=search_paths.typeshed_path + (os.path.join(here, 'stubs'), ),
        )
        super(MypyZopeBuildManager, self).__init__(
           data_dir, zope_search_paths, *args, **kwargs)


def monkey_patch_build_manager() -> None:
    build.BuildManager = MypyZopeBuildManager  # type: ignore


def plugin(version: str) -> PyType[Plugin]:
    # TODO: Submit a patch for mypy to allow customization of search paths for
    # plugins and remove monkeypatching
    monkey_patch_build_manager()
    return ZopeInterfacePlugin
