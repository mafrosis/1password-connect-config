export OP_CONNECT_TOKEN

.PHONY: test
test:
	./test/venv/bin/python test/fetch_secret.py
