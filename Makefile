.PHONY: installs requirements and run server

install: requirements.txt
	python3 -m pip install -U pip
	python3 -m pip install -r requirements.txt

clean:
	rm -r app/blockchain/__pycache__/
	rm -r app/__pycache__/

serve: install
	uvicorn app.main:app --host 127.0.0.1 --port 8000