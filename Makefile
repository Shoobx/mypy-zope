VE=ve
VEBIN=$(VE)/bin

all: $(VE)

$(VE): setup.py
	virtualenv -p python3 $(VE)
	$(VEBIN)/pip install -e .[test]

.PHONY: test
test:
	$(VEBIN)/pytest -v --cov src/mypy_zope --cov-report=html


# Mypy self-test
.PHONY: mypy
mypy:
	$(VEBIN)/mypy src/mypy_zope --strict

.PHONY: mypy-report
mypy-report:
	$(VEBIN)/mypy src/mypy_zope --strict --html-report reports/html --txt-report reports/txt
	cat reports/txt/index.txt
