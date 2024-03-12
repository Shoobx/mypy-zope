# Changelog

All notable changes to this project will be documented in this file.

## 1.0.4 (2024-03-12)
---------------------

- Drop support for python-3.7 (follow mypy). 
- Support for mypy up to 1.9.x


## 1.0.3 (2023-12-26)
---------------------

- Support for mypy up to 1.8.x


## 1.0.2 (2023-12-09)
---------------------

- Support for mypy up to 1.7.x


## 1.0.1 (2023-08-30)
---------------------

- Support for mypy up to 1.6.0


## 1.0.0 (2023-06-26)
------------------

- Support mypy up to 1.5.0


0.9.1 (2023-03-24)
------------------

- Follow semantic versioning in mypy version pins (#96)


0.9.0 (2023-02-10)
------------------

- Upgrade to Mypy-1.0.0 (#89)
- Fix caching error (Metaclass conflict) (#86) 


0.3.11 (2022-09-30)
-------------------

- Fix "Cannot determine consistent method resolution order (MRO)" error after
  repeated mypy runs (#80).


0.3.10 (2022-09-27)
-------------------

- Upgrade to Mypy-0.981.


0.3.9 (2022-07-19)
------------------

- Upgrade to Mypy-0.971.


0.3.8 (2022-06-08)
------------------

- Upgrade to Mypy-0.961.


0.3.7 (2022-04-28)
------------------

- Upgrade to Mypy-0.950.


0.3.6 (2022-03-15)
------------------

- Upgrade to Mypy-0.941.


0.3.5 (2022-01-11)
------------------

- Upgrade to Mypy-0.931.


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


0.2.9 - 2021-01-23
------------------

- Upgrade to Mypy-0.800
- Add support for Python 3.9.


0.2.8 - 2020-10-09
------------------

- Upgrade to Mypy-0.790


0.2.7 - 2020-06-19
------------------

- Upgrade to Mypy-0.770


0.2.6 - 2020-06-02
------------------

- Improved mypy annotations in Components methods


0.2.5 - 2020-03-12
------------------

- Upgrade to Mypy-0.770


0.2.4 - 2019-12-30
------------------

- Upgrade to Mypy-0.761
- Add support for Python 3.8.


0.2.3 - 2019-11-30
------------------

- Upgrade to Mypy-0.750


0.2.2 - 2019-10-28
------------------

- Upgrade to Mypy-0.740


0.2.1 - 2019-09-30
------------------

- Upgrade to Mypy-0.730
- Fixing crash while analyzing dynamically inherited class definitions (#11)


0.2.0 - 2019-08-03
------------------

- Support for Mypy-0.720.
- Avoid merging interface and implementation class hierarchies into single MRO.
- Implement implementation class validation against the declared interfaces.

0.1.3 - 2019-05-05
------------------

- Initial release.
