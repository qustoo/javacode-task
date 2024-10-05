DOCKER_COMPOSE := docker-compose
SERVICE_NAME := javacode-app
.PHONY: up down build logs sort flake8 black linters

up:
	$(DOCKER_COMPOSE) up --build -d
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

linters: sort black flake8