VE=ve
VEBIN=$(VE)/bin

all: $(VE)

$(VE): setup.py
	virtualenv -p python3 $(VE)
	$(VEBIN)/pip install -e .
