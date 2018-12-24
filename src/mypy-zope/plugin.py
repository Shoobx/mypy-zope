from mypy.types import (
    Type, Instance, CallableType, TypedDictType, UnionType, NoneTyp, TypeVarType,
    AnyType, TypeList, UnboundType, TypeOfAny, TypeType,
)
from mypy.plugin import (
    CallableType, CheckerPluginInterface, MethodSigContext, Plugin,
    AnalyzeTypeContext, FunctionContext, MethodContext, AttributeContext,
    ClassDefContext
)
from typing import Callable, Optional

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
        # def analyze(methodSigContext):
        #     # import ipdb; ipdb.set_trace()
        #     sig = methodSigContext.default_signature
        #     if methodSigContext.type.type.metadata.get('is_interface'):
        #         print("*** Using abstract sig", methodSigContext.default_signature)
        #         sig.definition.is_abstract = True
        #     return sig

        # if fullname.startswith('sample'):
        #     return analyze
        return None

    def get_method_hook(self, fullname: str
                        ) -> Optional[Callable[[MethodContext], Type]]:
        # print(f"get_method_hook: {fullname}")

        # def analyze(methodContext):
        #     import ipdb; ipdb.set_trace()
        #     tp = methodContext.type.type
        #     if not tp.metadata.get('is_interface'):
        #         return methodContext.default_return_type

        #     return methodContext.default_return_type


        # if fullname.startswith("sample"):
        #     return analyze
        return None

    def get_attribute_hook(self, fullname: str
                           ) -> Optional[Callable[[AttributeContext], Type]]:
        # print(f"get_attribute_hook: {fullname}")
        return None

    def get_class_decorator_hook(self, fullname: str
                                 ) -> Optional[Callable[[ClassDefContext], None]]:
        # print(f"get_class_decorator_hook: {fullname}")
        def analyze(classDefContext):
            api = classDefContext.api
            decor = classDefContext.reason
            iface_type = api.expr_to_analyzed_type(decor.args[0])
            # import ipdb; ipdb.set_trace()
            if not iface_type.type.metadata.get('is_interface'):
                api.fail("zope.interface.implementer accepts interface", decor)

            class_info = classDefContext.cls.info
            # print("CLASS INFO", class_info)
            class_info.metadata['implements'] = iface_type.type.fullname()
            print(f"*** Found implementation of {iface_type}: {class_info.fullname()}")
            # import ipdb; ipdb.set_trace()
            class_info.mro.append(iface_type.type)
            # import ipdb; ipdb.set_trace()

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
        def analyze(classDef):
            print(f"*** Found zope interface: {classDef.cls.fullname}")
            classDef.cls.info.metadata['is_interface'] = True
            classDef.cls.info.is_abstract = True
            # import ipdb; ipdb.set_trace()
            from mypy.nodes import Decorator, Var, Argument, ARG_POS
            for name, node in classDef.cls.info.names.items():
                func = node.node
                func.is_abstract = True
                func.is_decorated = True
                fakeself = Argument(
                    Var('self', None),
                    classDef.cls.info, None, ARG_POS)
                func.arg_names.insert(0, 'self')
                func.arg_kinds.insert(0, ARG_POS)
                func.arguments.insert(0, fakeself)

                func.type.arg_names.insert(0, 'self')
                func.type.arg_kinds.insert(0, ARG_POS)
                selftype = Instance(classDef.cls.info, [],
                                    line=classDef.cls.line,
                                    column=classDef.cls.column)
                func.type.arg_types.insert(0, selftype)

                # func.is_static = True
                var = Var(name, func.type)
                var.is_initialized_in_class=True
                # var.is_staticmethod = True
                var.info = func.info
                var.set_line(func.line)
                node.node = Decorator(func, [], var)

            # import ipdb; ipdb.set_trace()
            # cls.info.names['hello'].node.is_abstract=True

        if fullname == 'zope.interface.Interface':
            return analyze
            # import ipdb; ipdb.set_trace()
        return None

    def get_customize_class_mro_hook(self, fullname: str
                                     ) -> Optional[Callable[[ClassDefContext], None]]:
        # print(f"get_customize_class_mro_hook: {fullname}")
        def analyze(classDefContext):
            info = classDefContext.cls.info
            if not info.metadata.get('implements'):
                return

            api = classDefContext.api
            iface_expr = info.metadata['implements']
            # iface_type = api.expr_to_analyzed_type(iface_expr)
            stn = api.lookup_fully_qualified(iface_expr)
            print(f"*** Adding {iface_expr} to MRO of {info.fullname()}")
            info.mro.append(stn.node)
            api.calculate_abstract_status(info)

        return analyze

def plugin(version):
    return ZopeInterfacePlugin
