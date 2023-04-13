.ONESHELL:
SHELL := /bin/bash

help:
	@echo 'Usage: make [target] ...'
	@echo
	@echo 'targets:'
	@echo -e "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\\x1b[36m\1\\x1b[m:\2/' | column -c2 -t -s :)"

up: ## Starts the application containers
	@docker-compose up -d

down: ## Stops the application containers
	@docker-compose down

restart: ## Restarts the application containers
	@docker-compose restart

logs: ## Shows the application logs
	@docker-compose logs -f

clean: ## Removes all containers and images
	@docker-compose down --rmi all --volumes --remove-orphans

seed: ## Seeds the database
	@python delete_schema.py
	@python create_schema.py
	@python feed_database_with_mocks.py