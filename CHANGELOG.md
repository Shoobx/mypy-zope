# Changelog

All notable changes to this project will be documented in this file.

0.3.4 (2021-12-23)
------------------

- Upgrade to Mypy-0.930.


0.3.3 (2021-12-17)
------------------

- Declare support for Python-3.10.
- Upgrade to Mypy-0.920.


0.3.2 (2021-06-24)
------------------

- Upgrade to Mypy-0.910.


0.3.1 (2021-06-11)
------------------

- Upgrade to Mypy-0.902.


0.3.0 (2021-04-04)
------------------

- Support for `classImplements` declarations (#40).
- Support for `@overload` decorator in interfaces (#46)


0.2.13 (2021-03-23)
-------------------

- Fix "Cannot determine consistent method resolution order (MRO)" error (#34, #41)


0.2.12 (2021-03-13)
-------------------

- Better type inference for contextmanagers and open() function: do not override 
  the default behavior for tese cases
- Support interfaces defined inside classes

0.2.11 (2021-02-21)
-------------------

- Upgrade to Mypy-0.812.


0.2.10 (2021-01-27)
-------------------

- Avoid failure when handling metaclasses of unknown type (#28).


## [0.2.9] - 2021-01-23

- Upgrade to Mypy-0.800
- Add support for Python 3.9.


## [0.2.8] - 2020-10-09

- Upgrade to Mypy-0.790


## [0.2.7] - 2020-06-19

- Upgrade to Mypy-0.770


## [0.2.6] - 2020-06-02

- Improved mypy annotations in Components methods


## [0.2.5] - 2020-03-12

- Upgrade to Mypy-0.770


## [0.2.4] - 2019-12-30

- Upgrade to Mypy-0.761
- Add support for Python 3.8.


## [0.2.3] - 2019-11-30

- Upgrade to Mypy-0.750


## [0.2.2] - 2019-10-28

- Upgrade to Mypy-0.740


## [0.2.1] - 2019-09-30

- Upgrade to Mypy-0.730
- Fixing crash while analyzing dynamically inherited class definitions (#11)


## [0.2.0] - 2019-08-03

- Support for Mypy-0.720.
- Avoid merging interface and implementation class hierarchies into single MRO.
- Implement implementation class validation against the declared interfaces.

## [0.1.3] - 2019-05-05

- Initial release.

[Unreleased]: https://github.com/Shoobx/mypy-zope
[0.2.9]: https://github.com/Shoobx/mypy-zope/releases/tag/0.2.9
[0.2.8]: https://github.com/Shoobx/mypy-zope/releases/tag/0.2.8
[0.2.7]: https://github.com/Shoobx/mypy-zope/releases/tag/0.2.7
[0.2.6]: https://github.com/Shoobx/mypy-zope/releases/tag/0.2.6
[0.2.5]: https://github.com/Shoobx/mypy-zope/releases/tag/0.2.5
[0.2.4]: https://github.com/Shoobx/mypy-zope/releases/tag/0.2.4
[0.2.3]: https://github.com/Shoobx/mypy-zope/releases/tag/0.2.3
[0.2.2]: https://github.com/Shoobx/mypy-zope/releases/tag/0.2.2
[0.2.1]: https://github.com/Shoobx/mypy-zope/releases/tag/0.2.1
[0.2.0]: https://github.com/Shoobx/mypy-zope/releases/tag/0.2.0
[0.1.3]: https://github.com/Shoobx/mypy-zope/releases/tag/0.1.3
