VE=ve
VEBIN=$(VE)/bin

all: $(VE)

$(VE): setup.py
	virtualenv -p python3 $(VE)
	$(VEBIN)/pip install -e .

.PHONY: test
test:
	$(VEBIN)/pytest

# Mypy self-test
.PHONY: mypy
mypy:
	$(VEBIN)/mypy src --strict --html-report reports/html --txt-report reports/txt
	cat reports/txt/index.txt
