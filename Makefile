#   Makefile
#
.PHONY : clean

STORAGE := ${HOME}/wto-storage
MODULE_NAME := WorldTradeOrg
PACKAGE := WorldTradeOrg
PACKAGE_PREFIX := WorldTradeOrg
REQ_FILE := requirements.txt
REQ_FILE_TOOLS := requirements-tools.txt
PYTHON3 := $(shell which python3)
PIP3 := $(shell which pip3)
PYV3 := $(shell $(PYTHON3) -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)")

PWD := $(shell pwd)
SHELL:= /bin/bash
dockerfile=Dockerfile

module_name = $(MODULE_NAME)
EXPORT_VERSION = $(eval VERSION=$(shell cat .version))
.DEFAULT_GOAL : help

help: ## Show this help
	@printf "\n\033[33m%s:\033[1m\n" 'Available commands'
	@echo "======================================================"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[32m%-14s	\033[35;1m-- %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@printf "\033[33m%s\033[1m\n"
	@echo "======================================================"


envs: ## Print environment variables
	@echo "======================================================"
	@echo  "STORAGE: $(STORAGE)"
	@echo  "MODULE_NAME: $(MODULE_NAME)"
	@echo  "PACKAGE: $(PACKAGE)"
	@echo  "PACKAGE_PREFIX: $(PACKAGE_PREFIX)"
	@echo  "REQ_FILE: $(REQ_FILE)"
	@echo  "$(REQ_FILE_TOOLS)"
	@echo  "PYTHON3: $(PYTHON3)"
	@echo  "PIP3: $(PIP3)"
	@echo  "PYV3: $(PYV3)"
	@echo  "EXPORT_VERSION: $(EXPORT_VERSION)"
	@echo  "package $(PACKAGE)"
	@echo  "shell $(SHELL)"
	@echo  "python $(PYTHON3)"
	@echo  "pwd $(PWD)"
	@echo "======================================================"


clean: ## Cleaning the Directory
	@echo "======================================================"
	@echo clean $(PACKAGE)
	@echo "======================================================"
	rm -rf __pycache__ venv "*.pyc"
	find ./* -maxdepth 0 -name "*.pyc" -type f -delete

install-requirements: clean ## Install requirements
	@echo "======================================================"
	@echo "install-requirements $(PYV3) $(PACKAGE)"
	@echo "======================================================"
	$(PIP3) install --upgrade pip
	$(PIP3) install -r $(REQ_FILE)
	@echo "======================================================"


tools-requirements: $(REQ_FILE_TOOLS)
	@echo "======================================================"
	@echo "tools-requirements $(PYV3)"
	@echo "======================================================"
	$(PIP3) install --upgrade -r $(REQ_FILE_TOOLS)


run-infra: ## Run-infra (pull and run consul, postgres dockers)
	@docker-compose -f docker-compose.infra.yml up -d> /dev/null


stop-infra: ## Stop-infra (postgres dockers)
	@docker-compose -f docker-compose.infra.yml down>/dev/null


create-database: ## install-requirements run-infra ## Create postgres database and import schema
	@$(PYTHON3) ./Infra/scripts/create_database.py


load-data: ## Load_data to DataBase
	@$(PYTHON3) ./Infra/scripts/load_data.py


queryes: ## Script called RetrievingData/main.py
	@$(PYTHON3) ./RetrievingData/main.py


flake8:
	@echo "======================================================"
	@echo flake8 $(PACKAGE)
	@echo "======================================================"
	flake8 --ignore=F401,E265,E129


list: ## Makefile target list
	@echo "======================================================"
	@echo Makefile target list
	@echo "======================================================"
	@cat Makefile | grep "^[a-z]" | awk '{print $$1}' | sed "s/://g" | sort
