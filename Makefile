DOCKER_COMPOSE := docker-compose
DOCKER := docker
APP_NAME := javacode_fastapi_app
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
    $(DOCKER) exec $(APP_NAME) black .

sort:
   $(DOCKER) exec $(APP_NAME) isort .

flake8:
	$(DOCKER) exec $(APP_NAME) flake8 .

linters: sort black flake8