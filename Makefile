############################################################
##########  MAKEFILE FOR PYTHON-PROJECT-TEMPLATE  ##########
############################################################

#####################################
## Set PROJECT_PATH AND SHELL_PROFILE
#####################################
PROJECT_PATH=${PWD}
SHELL_PROFILE=${SHELL_PROFILE_PATH}

#######
## Init
#######
ifdef SHELL_PROFILE_PATH
init: poetry
	@echo "\033[0;35m####################\033[0m"
	@echo "\033[0;35m##  POETRY-SHELL  ##\033[0m"
	@echo "\033[0;35m####################\033[0m"
	@echo "Running shell..."
	@poetry shell
	@echo ""
else
init:
	@read -p "Your profile (.bashrc, .zshrc, .bash_profile, etc)?: " PROFILE; \
	echo "export SHELL_PROFILE_PATH='${HOME}/$$PROFILE'" >> ~/$$PROFILE; \
	echo "\033[0;33mSource your profile\033[0m";
endif

#########
## Commit
#########
commit:
	@echo "\033[0;35m##################\033[0m"
	@echo "\033[0;35m##  GIT COMMIT  ##\033[0m"
	@echo "\033[0;35m##################\033[0m"
	@echo "Running commitizen CHANGELOG.md update..."
	@git add .
	@echo ""
	@echo "Running commit..."
	@git commit
	@echo ""

##############
## Poetry init
##############
poetry:
	@echo "\033[0;35m######################\033[0m"
	@echo "\033[0;35m##  POETRY INSTALL  ##\033[0m"
	@echo "\033[0;35m######################\033[0m"
	@echo "Installing dependencies in poetry environment..."
	@poetry install --no-root
	@echo ""
	@echo "\033[0;35m##########################\033[0m"
	@echo "\033[0;35m##  PRE-COMMIT INSTALL  ##\033[0m"
	@echo "\033[0;35m##########################\033[0m"
	@echo "Installing pre-commit..."
	@poetry run pre-commit install
	@echo ""

poetry-remove:
	@echo "\033[0;35m#####################\033[0m"
	@echo "\033[0;35m##  POETRY REMOVE  ##\033[0m"
	@echo "\033[0;35m#####################\033[0m"
	@echo "Removing poetry environment $(shell poetry env list | awk '{print $$1}')..."
	@poetry env remove $(shell poetry env list | awk '{print $$1}')
	@echo "Poetry environment removed."
	@echo ""
	@echo "Removing poetry.lock..."
	@rm poetry.lock
	@echo "Poetry lock removed."
	@echo ""

#######
## Help
#######
help:
	@echo "#############################################################"
	@echo "##           MAKEFILE FOR PYTHON-PROJECT-TEMPLATE          ##"
	@echo "#############################################################"
	@echo ""
	@echo "   Targets:   "
	@echo ""
	@echo "   - init: Initialize repository:"
	@echo "     - Install poetry"
	@echo "     - Install pre-commit"
	@echo "       Usage: % make or % make init"
	@echo ""
	@echo "   - commit: Performs git add . and commit"
	@echo "       Usage: % make commit"
	@echo ""
	@echo "   - poetry-remove: Remove poetry environment."
	@echo "       Usage: % make poetry-remove"
	@echo ""
	@echo "   - default: init"
	@echo ""
	@echo "   Hidden targets:"
	@echo "   "
	@echo "   - poetry"
	@echo "   "
	@echo "#############################################################"
