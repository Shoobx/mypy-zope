import sys
from typing import List, Dict, Any, Callable, Optional
from typing import Type as PyType
from typing import cast

from mypy.types import (
    Type,
    Instance,
    CallableType,
    UnionType,
    NoneTyp,
    AnyType,
    TypeOfAny,
    PartialType,
)
from mypy.checker import TypeChecker, is_false_literal
from mypy.nodes import TypeInfo
from mypy.plugin import (
    CheckerPluginInterface,
    SemanticAnalyzerPluginInterface,
    MethodSigContext,
    Plugin,
    AnalyzeTypeContext,
    FunctionContext,
    MethodContext,
    AttributeContext,
    ClassDefContext,
)
from mypy.subtypes import find_member, is_subtype

from mypy.nodes import (
    Context,
    Var,
    Argument,
    FuncDef,
    CallExpr,
    RefExpr,
    Expression,
    ClassDef,
    Statement,
    Block,
    IndexExpr,
    MemberExpr,
    SymbolTable,
    SymbolTableNode,
    MDEF,
    ARG_POS,
    ARG_OPT,
    FUNC_NO_INFO,
)


def make_simple_type(
    fieldtype: str,
    arg_names: List[List[Optional[str]]],
    args: List[List[Expression]],
    api: CheckerPluginInterface,
) -> Optional[Type]:
    typename = SIMPLE_FIELD_TO_TYPE.get(fieldtype)
    if not typename:
        return None
    stdtype = api.named_generic_type(typename, [])
    for nameset, argset in zip(arg_names, args):
        for name, arg in zip(nameset, argset):
            if name == "required" and is_false_literal(arg):
                nonetype = NoneTyp()
                optionaltype = UnionType([stdtype, nonetype])
                return optionaltype
    return stdtype


FIELD_TO_TYPE_MAKER = {
    "zope.schema._bootstrapfields.Text": make_simple_type,
    "zope.schema._bootstrapfields.Bool": make_simple_type,
    "zope.schema._bootstrapfields.Complex": make_simple_type,
    "zope.schema._bootstrapfields.Real": make_simple_type,
    "zope.schema._bootstrapfields.Int": make_simple_type,
}

SIMPLE_FIELD_TO_TYPE = {
    "zope.schema._bootstrapfields.Text": "str",
    "zope.schema._bootstrapfields.Bool": "bool",
    "zope.schema._bootstrapfields.Complex": "complex",
    "zope.schema._bootstrapfields.Real": "float",
    "zope.schema._bootstrapfields.Int": "int",
}


class ZopeInterfacePlugin(Plugin):
    def log(self, msg: str) -> None:
        if self.options.verbosity >= 1:
            print("ZOPE:", msg, file=sys.stderr)

    def get_type_analyze_hook(
        self, fullname: str
    ) -> Optional[Callable[[AnalyzeTypeContext], Type]]:
        # print(f"get_type_analyze_hook: {fullname}")
        return None

    def get_function_hook(
        self, fullname: str
    ) -> Optional[Callable[[FunctionContext], Type]]:
        # print(f"get_function_hook: {fullname}")
        def analyze(function_ctx: FunctionContext) -> Type:
            # strtype = function_ctx.api.named_generic_type('builtins.str', [])
            # optstr = function_ctx.api.named_generic_type('typing.Optional', [strtype])
            api = function_ctx.api
            deftype = function_ctx.default_return_type

            if self._is_subclass(deftype, "zope.interface.interface.Attribute"):
                return self._get_schema_field_type(
                    deftype, function_ctx.arg_names, function_ctx.args, api
                )
            if self._is_subclass(deftype, "zope.schema.fieldproperty.FieldProperty"):
                # We cannot accurately determine the type, fallback to Any
                return AnyType(TypeOfAny.implementation_artifact)

            return deftype

        return analyze

    def get_method_signature_hook(
        self, fullname: str
    ) -> Optional[Callable[[MethodSigContext], CallableType]]:
        # print(f"get_method_signature_hook: {fullname}")
        return None

    def get_method_hook(
        self, fullname: str
    ) -> Optional[Callable[[MethodContext], Type]]:
        # print(f"get_method_hook: {fullname}")

        methodname = fullname.split(".")[-1]
        if methodname in ("providedBy", "implementedBy"):

            def analyze(method_ctx: MethodContext) -> Type:
                assert isinstance(method_ctx.context, CallExpr)
                assert isinstance(method_ctx.context.callee, MemberExpr)
                if method_ctx.context.callee.name == "providedBy":
                    method_ctx.context.callee.fullname = "builtins.isinstance"
                else:
                    method_ctx.context.callee.fullname = "builtins.issubclass"
                method_ctx.context.args = [
                    method_ctx.args[0][0],
                    method_ctx.context.callee.expr,
                ]

                return method_ctx.default_return_type

            return analyze

        def analyze_implementation(method_ctx: MethodContext) -> Type:
            deftype = method_ctx.default_return_type
            if not isinstance(method_ctx.context, ClassDef):
                return deftype

            impl_info = method_ctx.context.info
            if impl_info is FUNC_NO_INFO:
                return deftype

            impl_type = Instance(impl_info, [])
            md = self._get_metadata(impl_info)
            ifaces = cast(List[str], md.get("implements", []))
            for ifacename in ifaces:
                # iface_type = method_ctx.api.named_generic_type(ifacename, [])
                assert isinstance(method_ctx.api, TypeChecker)
                iface_type = self._lookup_type(ifacename, method_ctx.api)
                self._report_implementation_problems(
                    impl_type, iface_type, method_ctx.api, method_ctx.context
                )
            return deftype

        if fullname == "zope.interface.declarations.implementer.__call__":
            return analyze_implementation

        return None

    def get_attribute_hook(
        self, fullname: str
    ) -> Optional[Callable[[AttributeContext], Type]]:
        # print(f"get_attribute_hook: {fullname}")
        return None

    def get_class_decorator_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        # print(f"get_class_decorator_hook: {fullname}")

        def apply_interface(
            iface_arg: Expression,
            class_info: TypeInfo,
            api: SemanticAnalyzerPluginInterface,
            context: Context,
        ) -> None:
            if not isinstance(iface_arg, RefExpr):
                api.fail(
                    "Argument to implementer should be a ref expression", iface_arg
                )
                return
            iface_name = iface_arg.fullname
            if iface_name is None:
                # unknown interface, probably from stubless package
                return

            iface_type = iface_arg.node
            if iface_type is None:
                return
            if not isinstance(iface_type, TypeInfo):
                # Possibly an interface from unimported package, ignore
                return

            if not self._is_interface(iface_type):
                api.fail(
                    f"zope.interface.implementer accepts interface, "
                    f"not {iface_name}.",
                    iface_arg,
                )
                api.fail(
                    f"Make sure you have stubs for all packages that "
                    f"provide interfaces for {iface_name} class hierarchy.",
                    iface_arg,
                )
                return

            # print("CLASS INFO", class_info)
            md = self._get_metadata(class_info)
            if "implements" not in md:
                md["implements"] = []
            # impl_list = cast(List[str], md['implements'])
            md["implements"].append(iface_type.fullname())
            self.log(
                f"Found implementation of "
                f"{iface_type.fullname()}: {class_info.fullname()}"
            )

            # Make sure implementation is treates subtype of an interface. Pretend
            # there is a decorator for the class that will create a "type promotion"
            faketi = TypeInfo(SymbolTable(), iface_type.defn, iface_type.module_name)
            faketi._promote = Instance(iface_type, [])
            class_info.mro.append(faketi)

        def analyze(classdef_ctx: ClassDefContext) -> None:
            api = classdef_ctx.api

            decor = cast(CallExpr, classdef_ctx.reason)

            for iface_arg in decor.args:
                apply_interface(iface_arg, classdef_ctx.cls.info, api, decor)

        if fullname == "zope.interface.declarations.implementer":
            return analyze
        return None

    def get_metaclass_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        # print(f"get_metaclass_hook: {fullname}")
        return None

    def get_base_class_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        # print(f"get_base_class_hook: {fullname}")
        def analyze_direct(classdef_ctx: ClassDefContext) -> None:
            self.log(f"Found zope interface: {classdef_ctx.cls.fullname}")
            md = self._get_metadata(classdef_ctx.cls.info)
            md["is_interface"] = True

        def analyze_subinterface(classdef_ctx: ClassDefContext) -> None:
            # If one of the bases is an interface, this is also an interface
            if isinstance(classdef_ctx.reason, IndexExpr):
                # Generic parameterised interface
                reason = classdef_ctx.reason.base
            else:
                reason = classdef_ctx.reason
            if not isinstance(reason, RefExpr):
                return
            cls_info = classdef_ctx.cls.info

            api = classdef_ctx.api
            base_name = reason.fullname
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
                cls_md["is_interface"] = True

        if fullname == "zope.interface.interface.Interface":
            return analyze_direct

        return analyze_subinterface

    def get_customize_class_mro_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        # print(f"get_customize_class_mro_hook: {fullname}")

        def analyze_interface_base(classdef_ctx: ClassDefContext) -> None:
            # Create fake constructor to mimic adaptation signature
            info = classdef_ctx.cls.info
            api = classdef_ctx.api
            if "__init__" in info.names:
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
                arg_names=["self", "obj", "alternate"],
                ret_type=NoneTyp(),
                fallback=api.named_type("function"),
            )
            newinit = FuncDef("__init__", [], Block([]), init_fn)
            newinit.info = info
            info.names["__init__"] = SymbolTableNode(
                MDEF, newinit, plugin_generated=True
            )

        def analyze(classdef_ctx: ClassDefContext) -> None:
            info = classdef_ctx.cls.info

            # If we are dealing with an interface, massage it a bit, e.g.
            # inject `self` argument to all methods
            directiface = "zope.interface.interface.Interface" in [
                b.type.fullname() for b in info.bases
            ]
            subinterface = any(self._is_interface(b.type) for b in info.bases)
            if directiface or subinterface:
                self._analyze_zope_interface(classdef_ctx.api, classdef_ctx.cls)

        if fullname == "zope.interface.interface.Interface":
            return analyze_interface_base

        return analyze

    def _is_subclass(self, typ: Type, classname: str) -> bool:
        if not isinstance(typ, Instance):
            return False

        parent_names = [t.fullname() for t in typ.type.mro]
        return classname in parent_names

    def _get_schema_field_type(
        self,
        typ: Type,
        arg_names: List[List[Optional[str]]],
        args: List[List[Expression]],
        api: CheckerPluginInterface,
    ) -> Type:
        """Given subclass of zope.interface.Attribute, determine python
        type that would correspond to it.
        """
        # If we are not processing an interface, leave the type as is
        assert isinstance(api, TypeChecker)
        scopecls = api.scope.active_class()
        if scopecls is None:
            return typ

        if not self._is_interface(scopecls):
            return typ

        # If default type is a zope.schema.Field, we should convert it to a
        # python type
        if not isinstance(typ, Instance):
            return typ

        parent_names = [t.fullname() for t in typ.type.mro]

        # If it is a konwn field, build a python type out of it
        for clsname in parent_names:
            maker = FIELD_TO_TYPE_MAKER.get(clsname)
            if maker is None:
                continue

            convtype = maker(clsname, arg_names, args, api)
            if convtype:
                self.log(
                    f"Converting a field {typ} into type {convtype} "
                    f"for {scopecls.fullname()}"
                )
                return convtype

        # For unknown fields, just return ANY
        self.log(f"Unknown field {typ} in interface {scopecls.fullname()}")
        return AnyType(
            TypeOfAny.implementation_artifact, line=typ.line, column=typ.column
        )

    def _analyze_zope_interface(
        self, api: SemanticAnalyzerPluginInterface, cls: ClassDef
    ) -> None:
        self.log(f"Adjusting zope interface: {cls.info.fullname()}")
        md = self._get_metadata(cls.info)
        # Even though interface is abstract, we mark it as non-abstract to
        # allow adaptation pattern: IInterface(context)
        if md.get("interface_analyzed", False):
            return

        for idx, item in enumerate(cls.defs.body):
            if not isinstance(item, FuncDef):
                continue

            replacement = self._adjust_interface_function(api, cls.info, item)
            cls.defs.body[idx] = replacement

        md["interface_analyzed"] = True

    def _get_metadata(self, typeinfo: TypeInfo) -> Dict[str, Any]:
        if "zope" not in typeinfo.metadata:
            typeinfo.metadata["zope"] = {}
        return typeinfo.metadata["zope"]

    def _is_interface(self, typeinfo: TypeInfo) -> bool:
        md = self._get_metadata(typeinfo)
        return md.get("is_interface", False)

    def _adjust_interface_function(
        self,
        api: SemanticAnalyzerPluginInterface,
        class_info: TypeInfo,
        func_def: FuncDef,
    ) -> Statement:

        if func_def.arg_names and func_def.arg_names[0] == "self":
            # reveal the common mistake of leaving "self" arguments in the
            # interface
            api.fail("Interface methods should not have 'self' argument", func_def)
        else:
            selftype = Instance(
                class_info, [], line=class_info.line, column=class_info.column
            )
            selfarg = Argument(Var("self", None), selftype, None, ARG_POS)

            if isinstance(func_def.type, CallableType):
                func_def.type.arg_names.insert(0, "self")
                func_def.type.arg_kinds.insert(0, ARG_POS)
                func_def.type.arg_types.insert(0, selftype)
            func_def.arg_names.insert(0, "self")
            func_def.arg_kinds.insert(0, ARG_POS)
            func_def.arguments.insert(0, selfarg)

        return func_def

    def _report_implementation_problems(
        self,
        class_type: Instance,
        iface_type: Instance,
        api: CheckerPluginInterface,
        context: Context,
    ) -> None:
        # This mimicks mypy's MessageBuilder.report_protocol_problems with
        # simplifications for zope interfaces.
        class_info = class_type.type
        iface_info = iface_type.type
        interface_members = self._get_interface_members(iface_info)

        # Report missing members
        missing = []
        for member in interface_members:
            if find_member(member, class_type, class_type) is None:
                missing.append(member)

        if missing:
            missing_fmt = ", ".join(missing)
            api.fail(
                f"'{class_info.name()}' is missing following "
                f"'{iface_info.name()}' interface members: {missing_fmt}.",
                context,
            )

        # Report member type conflicts
        conflicts = []  # tuple of (name, got, expected)
        for member in interface_members:
            iface_member_type = find_member(member, iface_type, iface_type)
            assert iface_member_type is not None
            impl_member_type = find_member(member, class_type, class_type)
            if impl_member_type is None:
                continue

            if isinstance(impl_member_type, PartialType):
                # We don't know how to deal with partial type here. Partial
                # types will be resolved later when the implementation class is
                # fully type-checked. We are doing our job before that, so all
                # we can do is to skip checking of such members.
                continue

            is_compat = is_subtype(
                impl_member_type, iface_member_type, ignore_pos_arg_names=True
            )
            if not is_compat:
                conflicts.append((member, impl_member_type, iface_member_type))

        if conflicts:
            api.fail(f'Invalid implementation of "{iface_info.name()}"', context)
            for name, got, expected in conflicts:
                fmt_got, fmt_expected = api.msg.format_distinctly(got, expected)
                if isinstance(got, CallableType):
                    fmt_got = api.msg.pretty_callable(got)
                else:
                    fmt_got = api.msg.format(got)

                if isinstance(expected, CallableType):
                    fmt_expected = api.msg.pretty_callable(expected)
                else:
                    fmt_expected = api.msg.format(expected)

                api.fail(
                    f"Incompatible implementation of '{iface_info.name()}.{name}': "
                    f"Got {fmt_got}; expected {fmt_expected}",
                    got,
                )

    def _lookup_type(self, fullname: str, api: TypeChecker) -> Instance:
        # Implement own type lookup, because TypeChecker.named_generic_type is
        # dysfunctional
        parts = fullname.split(".")
        module_name = ".".join(parts[:-1])
        type_name = parts[-1]
        module = api.modules[module_name]
        sym = module.names[type_name]
        typeinfo = sym.node
        assert isinstance(typeinfo, TypeInfo)
        any_type = AnyType(TypeOfAny.from_omitted_generics)
        return Instance(typeinfo, [any_type] * len(typeinfo.defn.type_vars))

    def _get_interface_members(self, iface_info: TypeInfo) -> List[str]:
        members = set()
        # we skip "object" and "Interface" since everyone implements it
        for base in iface_info.mro[:-2]:
            for name in base.names:
                members.add(name)
        return sorted(list(members))


def plugin(version: str) -> PyType[Plugin]:
    return ZopeInterfacePlugin
