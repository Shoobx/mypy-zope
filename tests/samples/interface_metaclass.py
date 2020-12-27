from zope.interface import interface


class RemoteInterface(metaclass=interface.InterfaceClass):
    pass


class Api(RemoteInterface):
    def open():
        "open something"
