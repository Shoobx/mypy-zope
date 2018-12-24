from typing import Dict, Any, Callable, Optional
from typing import Type as PyType
from typing import cast

from mypy.types import (
    Type, Instance, CallableType, TypedDictType, UnionType, NoneTyp, TypeVarType,
    AnyType, TypeList, UnboundType, TypeOfAny, TypeType
)
from mypy.nodes import TypeInfo
from mypy.plugin import (
    CallableType, CheckerPluginInterface, MethodSigContext, Plugin,
    AnalyzeTypeContext, FunctionContext, MethodContext, AttributeContext,
    ClassDefContext
)
from mypy.semanal import SemanticAnalyzerPass2

from mypy.nodes import (
    Decorator, Var, Argument, FuncDef, CallExpr, NameExpr, ARG_POS
)


class ZopeInterfacePlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str
                              ) -> Optional[Callable[[AnalyzeTypeContext], Type]]:
        # print(f"get_type_analyze_hook: {fullname}")
        return None

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        # print(f"get_function_hook: {fullname}")
        return None

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
        def analyze(classdef_ctx: ClassDefContext) -> None:
            api = classdef_ctx.api

            decor = cast(CallExpr, classdef_ctx.reason)
            if len(decor.args) !=1:
                api.fail(f"Implementer should accept one interface", decor)
                return
            if not isinstance(decor.args[0], NameExpr):
                api.fail("Argument to implementer should be a name expression",
                         decor)
                return
            iface_name = decor.args[0].fullname
            if iface_name is None:
                api.fail("Interface should be specified", decor)
                return
            iface_node = api.lookup_fully_qualified(iface_name)
            iface_type = cast(TypeInfo, iface_node.node)

            md = self._get_metadata(iface_type)
            if not md.get('is_interface'):
                api.fail("zope.interface.implementer accepts interface", decor)
                return

            class_info = classdef_ctx.cls.info
            # print("CLASS INFO", class_info)
            md = self._get_metadata(class_info)
            md['implements'] = iface_type.fullname()
            print(f"*** Found implementation of {iface_type.fullname()}: {class_info.fullname()}")
            class_info.mro.append(iface_type)

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
            print(f"*** Found zope interface: {classdef_ctx.cls.fullname}")
            md = self._get_metadata(classdef_ctx.cls.info)
            md['is_interface'] = True
            self._process_zope_interface(classdef_ctx.cls.info)

        def analyze_subinterface(classdef_ctx: ClassDefContext) -> None:
            # If one of the bases is an interface, this is also an interface
            if not isinstance(classdef_ctx.reason, NameExpr):
                return
            cls_info = classdef_ctx.cls.info
            cls_md = self._get_metadata(cls_info)
            api = classdef_ctx.api
            base_name = classdef_ctx.reason.fullname
            if not base_name:
                return
            base_node = api.lookup_fully_qualified_or_none(base_name)
            if not base_node:
                return

            base_info = cast(TypeInfo, base_node.node)
            base_md = self._get_metadata(base_info)
            if base_md.get('is_interface'):
                print(f"*** Found zope subinterface: {cls_info.fullname()}")
                cls_md['is_interface'] = True
                self._process_zope_interface(cls_info)

        if fullname == 'zope.interface.Interface':
            return analyze_direct

        # if fullname == 'interface_inheritance.ISomething':
        return analyze_subinterface
        # return None

    def get_customize_class_mro_hook(self, fullname: str
                                     ) -> Optional[Callable[[ClassDefContext], None]]:
        # print(f"get_customize_class_mro_hook: {fullname}")
        def analyze(classdef_ctx: ClassDefContext) -> None:
            info = classdef_ctx.cls.info
            md = self._get_metadata(info)
            iface_expr = cast(str, md.get('implements'))
            if not iface_expr:
                return

            # iface_type = api.expr_to_analyzed_type(iface_expr)
            stn = classdef_ctx.api.lookup_fully_qualified(iface_expr)
            print(f"*** Adding {iface_expr} to MRO of {info.fullname()}")
            info.mro.extend(cast(TypeInfo, stn.node).mro)

            # XXX: Reuse abstract status checker from SemanticAnalyzerPass2.
            # Ideally, implement a dedicated interface verifier.
            api = cast(SemanticAnalyzerPass2, classdef_ctx.api)
            api.calculate_abstract_status(info)

        return analyze

    def _get_metadata(self, typeinfo: TypeInfo) -> Dict[str, Any]:
        if 'zope' not in typeinfo.metadata:
            typeinfo.metadata['zope'] = {}
        return typeinfo.metadata['zope']

    def _process_zope_interface(self, type_info: TypeInfo) -> None:
        type_info.is_abstract = True
        for name, node in type_info.names.items():
            if not isinstance(node.node, FuncDef):
                continue
            selftype = Instance(type_info, [],
                                line=type_info.line,
                                column=type_info.column)
            selfarg = Argument(Var('self', None), selftype, None, ARG_POS)

            func = node.node
            func.is_abstract = True
            func.is_decorated = True
            func.arg_names.insert(0, 'self')
            func.arg_kinds.insert(0, ARG_POS)
            func.arguments.insert(0, selfarg)

            if isinstance(func.type, CallableType):
                func.type.arg_names.insert(0, 'self')
                func.type.arg_kinds.insert(0, ARG_POS)
                func.type.arg_types.insert(0, selftype)

            # func.is_static = True
            var = Var(name, func.type)
            var.is_initialized_in_class=True
            # var.is_staticmethod = True
            var.info = func.info
            var.set_line(func.line)
            node.node = Decorator(func, [], var)

        pass

def plugin(version: str) -> PyType[Plugin]:
    return ZopeInterfacePlugin
