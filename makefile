run:
	python src/main.py
test:
	pytest tests/
lint:
	flake8 src/
format:
	black src/
