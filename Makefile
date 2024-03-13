.PHONY: prepare 
prepare:
	python3 -m venv env 
	./env/bin/pip install -r requirements.txt 

.PHONY: run 
run:
	./env/bin/python3 tg_bot/main.py 
