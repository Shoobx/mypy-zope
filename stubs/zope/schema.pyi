from zope.interface import Attribute

class Field(Attribute):
    def __init__(self, title='', description='', __name__='',
                 required=True, readonly=False, constraint=None, default=None,
                 defaultFactory=None, *args, **kwargs) -> None:
        ...

class Text(Field): ...
class TextLine(Text): ...