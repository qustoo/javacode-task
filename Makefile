DOCKER_COMPOSE := docker-compose
SERVICE_NAME := javacode-app
.PHONY: up down build logs linter sort flake8 black linters locally_start

up:
	$(DOCKER_COMPOSE) up -d
down:
	$(DOCKER_COMPOSE) down

build:
	$(DOCKER_COMPOSE) build

logs:
	$(DOCKER_COMPOSE) logs -f

black:
    $(DOCKER_COMPOSE) exec $(SERVICE_NAME) isort .

sort:
   $(DOCKER_COMPOSE) exec $(SERVICE_NAME) isort .

flake8:
	$(DOCKER_COMPOSE) exec $(SERVICE_NAME) flake8 .

locally-run:
    bash locally_run.sh

linters: sort black flake8