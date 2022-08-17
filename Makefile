.PHONY: installs requirements and run server

PYTHON=${VENV_NAME}/bin/python

install: prepare_venv

prepare_venv: $(VENV_NAME)/bin/activate

$(VENV_NAME)/bin/activate: requirements.txt
	python -m venv venv 
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r requirements.txt
	touch $(VENV_NAME)/bin/activate

clean_blockchain:
	rm -r app/blockchain/__pycache__/

clean_app:
	rm -r app/__pycache__/

serve: prepare_venv
	CREDENTIALS_PATH="app/secrets/credentials.json" ${PYTHON} -m  uvicorn app.main:app --host 127.0.0.1 --port 8000

