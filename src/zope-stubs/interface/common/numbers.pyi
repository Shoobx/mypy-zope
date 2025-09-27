import numbers as abc
from zope.interface.common import ABCInterface as ABCInterface, optional as optional

class INumber(ABCInterface):
    abc = abc.Number

class IComplex(INumber):
    abc = abc.Complex
    def __complex__() -> complex: ...

class IReal(IComplex):
    abc = abc.Real
    def __complex__() -> complex: ...
    __floor__ = __complex__
    __ceil__ = __complex__

class IRational(IReal):
    abc = abc.Rational

class IIntegral(IRational):
    abc = abc.Integral
