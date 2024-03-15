########################################################################################
##########  MAKEFILE FOR {{cookiecutter.project.upper()}}  ##########
########################################################################################

#####################################
## Set PROJECT_PATH AND SHELL_PROFILE
#####################################
PROJECT_PATH=${PWD}
SHELL_PROFILE=${SHELL_PROFILE_PATH}
JUPYTERLAB=${JUPYTERLAB_DIR}

#######
## Init
#######
ifdef SHELL_PROFILE_PATH
init: poetry paths docker
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

#################
## Change version
#################
change-version:
	@echo "\033[0;35m######################\033[0m"
	@echo "\033[0;35m##  CHANGE VERSION  ##\033[0m"
	@echo "\033[0;35m######################\033[0m"
ifdef version
	@old_version=$(shell cat pyproject.toml | awk '/^version =/{print $$3}' | xargs); \
	echo "Changing from version v$$old_version to v${version}..."; \
	sed "s/tree\/v$$old_version/tree\/v${version}/g" mkdocs.yml > temp && mv temp mkdocs.yml; \
	sed "s/@v$$old_version/@v${version}/g" mkdocs.yml > temp && mv temp mkdocs.yml; \
	sed "s/\/v$$old_version/\/v${version}/g" README.md > temp && mv temp README.md; \
	sed "s/@v$$old_version/@v${version}/g" README.md > temp && mv temp README.md;
	sed "s/@v$$old_version/@v${version}/g" docs/index.md > temp && mv temp docs/index.md;
	@cat pyproject.toml | awk '/^version =/{gsub($$3,"\"${version}\"")};{print}' > temp && mv temp pyproject.toml
	@cat docs/design_doc.md | awk '/- Versión:/{gsub($$3,"${version}")};{print}' > temp && mv temp docs/design_doc.md
	@cat {{cookiecutter.project}}/__init__.py | awk '/^__version__ =/{gsub($$3,"\"${version}\"")};{print}' > temp && mv temp {{cookiecutter.project}}/__init__.py
	@cat tests/test_{{cookiecutter.project}}.py | awk '/__version__ ==/{gsub($$4,"\"${version}\"")};{print}' > temp && mv temp tests/test_{{cookiecutter.project}}.py
	@echo ""
	@echo "\033[0;35m##################\033[0m"
	@echo "\033[0;35m##  DOC DEPLOY  ##\033[0m"
	@echo "\033[0;35m##################\033[0m"
	@echo "Deploying documentation for version ${version}"
	@poetry run mike deploy v${version} -b gh-pages --push
	@poetry run mike set-default v${version}
	@echo ""
else
	@echo "\033[0;31mPlease set the version number:\033[0m \033[1;39m $$ make change-version version=<version_number>\033[0m"
	@echo ""
endif

#########
## Commit
#########
commit: pre-commit
	@echo "\033[0;35m##################\033[0m"
	@echo "\033[0;35m##  GIT COMMIT  ##\033[0m"
	@echo "\033[0;35m##################\033[0m"
	@echo "Running commitizen CHANGELOG.md update..."
	@poetry run cz changelog
	@git add .
	@echo ""
	@echo "Running comitizen commit..."
	@poetry run pre-commit run
	@poetry run cz commit
	@echo ""

#########
## Docker
#########
docker:
	@echo "\033[0;35m#######################\033[0m"
	@echo "\033[0;35m##  DOCKER SERVICES  ##\033[0m"
	@echo "\033[0;35m#######################\033[0m"
	@echo "Checking for Docker services..."
	@echo "\033[0;32mNo Docker services needed.\033[0m"
	@echo ""

################
## Documentation
################
doc-deploy:
	@echo "\033[0;35m##################\033[0m"
	@echo "\033[0;35m##  DOC DEPLOY  ##\033[0m"
	@echo "\033[0;35m##################\033[0m"
ifdef version
	@echo "Deploying documentation for version ${version}"
	@poetry run mike deploy v${version} -b gh-pages --push
	@poetry run mike set-default v${version}
	@echo ""
else
	@version=$(shell cat pyproject.toml | awk '/^version =/{print $$3}' | xargs); \
	echo "Deploying documentation for version $$version"; \
	poetry run mike deploy v$$version -b gh-pages --push; \
	poetry run mike set-default v$$version && echo "\033[0;32mDocumentation deployed successfully.\033[0m" || echo "\033[0;31mAn error has ocurred while deploying documentation\033[0m"
	@echo ""
endif

doc-serve:
	@echo "\033[0;35m#################\033[0m"
	@echo "\033[0;35m##  DOC SERVE  ##\033[0m"
	@echo "\033[0;35m#################\033[0m"
	@echo "Deploying documentation in localhost..."
	@poetry run mkdocs serve
	@echo ""

###################
## Jupyter Notebook
###################
jupyter:
	@echo "\033[0;35m###################\033[0m"
	@echo "\033[0;35m##  JUPYTER-LAB  ##\033[0m"
	@echo "\033[0;35m###################\033[0m"
	@echo "Deploying Jupyter-Lab in localhost..."
	@poetry run jupyter-lab
	@echo ""

#################################
## Exported environment variables
#################################
paths:
	@echo "\033[0;35m#####################\033[0m"
	@echo "\033[0;35m##  ENV VARIABLES  ##\033[0m"
	@echo "\033[0;35m#####################\033[0m"
	@echo "Checking for environment variables..."
	@echo "\033[0;32mNo environment variables needed.\033[0m"
	@echo ""

##############
## Poetry init
##############
poetry:
	@echo "\033[0;35m######################\033[0m"
	@echo "\033[0;35m##  POETRY INSTALL  ##\033[0m"
	@echo "\033[0;35m######################\033[0m"
	@echo "Installing dependencies in poetry environment..."
	@poetry install
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

#############
## Pre-commit
#############
pre-commit:
	@echo "\033[0;35m##################\033[0m"
	@echo "\033[0;35m##  PRE-COMMIT  ##\033[0m"
	@echo "\033[0;35m##################\033[0m"
	@cd ${PROJECT_PATH}/
	@git add .
	@pre-commit run
	@echo ""

pre-commit-all:
	@echo "\033[0;35m######################\033[0m"
	@echo "\033[0;35m##  PRE-COMMIT-ALL  ##\033[0m"
	@echo "\033[0;35m######################\033[0m"
	@cd ${PROJECT_PATH}/
	@git add .
	@pre-commit run
	@poetry run pre-commit run --all-files trailing-whitespace
	@poetry run pre-commit run --all-files check-executables-have-shebangs
	@poetry run pre-commit run --all-files debug-statements
	@poetry run pre-commit run --all-files check-merge-conflict
	@poetry run pre-commit run --all-files name-tests-test
	@poetry run pre-commit run --all-files ruff
	@poetry run pre-commit run --all-files flake8
	@poetry run pre-commit run --all-files black
	@poetry run pre-commit run --all-files bandit
	@poetry run pre-commit run --all-files isort

#######################
## Performance Analysis
########################
profile:
	@echo "\033[0;35m############################\033[0m"
	@echo "\033[0;35m##  PERFORMANCE ANALYSIS  ##\033[0m"
	@echo "\033[0;35m############################\033[0m"
ifdef version
	@echo "Running performance analysis for version v${version}..."
	@poetry run python ${PROJECT_PATH}/profiling/{{cookiecutter.project}}_profiling.py > docs/img/memory_profiler_v${version}.log
	@echo "Profiling log saved in docs/img/memory_profiler_v${version}.log"
	@mv plot.png docs/img/memory_profiler_plot_v${version}.png
	@echo "Memory and CPU usage reported in docs/img/memory_profiler_plot_v${version}.png"
	@echo ""
else
	@echo "Running performance análisis..."
	@poetry run python ${PROJECT_PATH}/profiling/{{cookiecutter.project}}_profiling.py > profiling/memory_profiler.log && echo "\033[0;32mProfiling log saved in profiling/memory_profiler.log.\033[0m" || echo "\033[0;31mError running performance analysis.\033[0m"
	@mv plot.png profiling/memory_profiler_plot.png
	@echo "\033[0;32mMemory and CPU usage reported in profiling/memory_profiler_plot.png.\033[0m"
	@echo ""
endif

############
## Streamlit
############
stream:
	@echo "\033[0;35m#####################\033[0m"
	@echo "\033[0;35m##  STREAMLIT-APP  ##\033[0m"
	@echo "\033[0;35m#####################\033[0m"
ifdef ip
	@cd ${PROJECT_PATH}/app;\
	echo "Deploying local Streamlit App in IP ${ip}..."; \
	poetry run streamlit run 01_✨_Model_App.py --server.port=8601 --server.enableCORS=false --server.enableXsrfProtection=false --theme.base=dark --theme.primaryColor=#9333ea --theme.font=monospace --theme.textColor=#f1f5f9 --server.fileWatcherType=none --browser.serverAddress=${ip}
else
	@cd ${PROJECT_PATH}/app;\
	echo "Deploying local Streamlit App..."; \
	poetry run streamlit run 01_✨_Model_App.py --server.port=8601 --server.enableCORS=false --server.enableXsrfProtection=false --theme.base=dark --theme.primaryColor=#9333ea --theme.font=monospace --theme.textColor=#f1f5f9 --server.fileWatcherType=none
endif

#############
## Unit Tests
#############
test:
	@echo "\033[0;35m##################\033[0m"
	@echo "\033[0;35m##  UNIT-TESTS  ##\033[0m"
	@echo "\033[0;35m##################\033[0m"
	@echo "Running unit tests..."
	@poetry run coverage run -m pytest ${PROJECT_PATH}/tests/
	@poetry run coverage html -d docs/coverage --omit="*cache*"
	@echo ""

#######
## Help
#######
help:
	@echo "#############################################################"
	@echo "##          MAKEFILE FOR {{cookiecutter.project.upper()}}          ##"
	@echo "#############################################################"
	@echo ""
	@echo "   Targets:   "
	@echo ""
	@echo "   - init: Initialize repository:"
	@echo "     - Install poetry"
	@echo "     - Install pre-commit"
	@echo "     - Check necessary paths and external dependencies"
	@echo "       Usage: % make init"
	@echo ""
	@echo "   - aliases: Create alias"
	@echo "       Usage: % make aliases"
	@echo ""
	@echo "   - change-version: Change version"
	@echo "       Usage: % make change-version version=<version_number>"
	@echo ""
	@echo "   - commit: Git commit changes with commitizen"
	@echo "       Usage: % make commit"
	@echo ""
	@echo "   - doc: Deploy documentation"
	@echo "       Usage: % make doc-deploy → GitHub Page"
	@echo "       Usage: % make doc-deploy version=<version_number> → GitHub Page"
	@echo "       Usage: % make doc-serve  → Local"
	@echo ""
	@echo "   - jup2md: Convert Jupyter notebook to Markdown"
	@echo "       Usage: % make jup2md → Convert notebooks/examples.md"
	@echo "       Usage: % make jup2md jupfile=</path/to/jupfile>"
	@echo "                            ↳ Convert notebooks/examples.md"
	@echo ""
	@echo "   - poetry-remove: Remove poetry environment."
	@echo "       Usage: % make poetry-remove"
	@echo ""
	@echo "   - pre-commit: Run pre-commits"
	@echo "       Usage: % make pre-commit"
	@echo ""
	@echo "   - profile: Run memory-profiler"
	@echo "       Usage: % make profile"
	@echo "       Usage: % make profile version=<version_number>"
	@echo ""
	@echo "   - test: Run pytests"
	@echo "       Usage: % make test"
	@echo ""
	@echo "   - stream: Run streamlit app"
	@echo "       Usage: % make stream"
	@echo ""
	@echo "   - help: Display this menu"
	@echo "       Usage: % make help"
	@echo ""
	@echo "   - default: init"
	@echo ""
	@echo "   Hidden targets:"
	@echo "   "
	@echo "   - poetry"
	@echo "   "
	@echo "#############################################################"
