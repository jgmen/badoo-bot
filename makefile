DOCKER_COMPOSE := $(shell command -v docker-compose 2>/dev/null || command -v podman-compose 2>/dev/null)

ifeq ($(DOCKER_COMPOSE),)
$(error No docker-compose or podman-compose command found in PATH)
endif

PYTHON = python
REDIS = redis-cache
SRC = src/
TESTS = tests/
APP = src/main.py

.PHONY: run run-docker dev redis-up redis-down test lint format clean logs shell stop-redis

run:
	$(PYTHON) $(APP)

run-dev:
	$(DOCKER_COMPOSE) up

stop-dev:
	$(DOCKER_COMPOSE) down

build:
	$(DOCKER_COMPOSE) up --build

redis-up:
	$(DOCKER_COMPOSE) up -d $(REDIS)

redis-down:
	$(DOCKER_COMPOSE) stop $(REDIS)

test:
	pytest $(TESTS)

lint:
	flake8 $(SRC)

format:
	black $(SRC)

clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf .pytest_cache

logs:
	$(DOCKER_COMPOSE) logs -f app

shell:
	$(DOCKER_COMPOSE) exec app /bin/bash

stop-redis:
	$(DOCKER_COMPOSE) stop $(REDIS)
