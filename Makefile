VENV ?= env
PIP ?= $(VENV)/bin/pip

help:
	@echo "  help         this list"
	@echo "  clean        delete virtualenv directory $(VENV)"
	@echo "  prepare-venv install virtualenv and requiements into directory $(VENV)"

clean:
	rm -rf env

prepare-venv:
	virtualenv $(VENV) --no-pip
	$(VENV)/bin/easy_install pip==10.0.1
	$(PIP) install -r requirements.txt
