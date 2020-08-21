.PHONY: clean data lint requirements sync_data_to_s3 sync_data_from_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = [OPTIONAL] your-bucket-for-syncing-data (do not include 's3://')
PROFILE = default
PROJECT_NAME = coronaBreakSuck2020Dash
PYTHON_INTERPRETER = python3


ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################

date_str = $(shell date +%Y-%m-%d -d "1 days ago")

## Install Python Dependencies
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Save current requirements
freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt

## Pull data from coronaBreakSuck2020
pull_data:
	cp -r ../coronaBreakSuck2020/data/topicmodels ./data/
	cp ../coronaBreakSuck2020/data/raw/$(date_str)/conf_global.csv ./data/
	cp ../coronaBreakSuck2020/data/raw/$(date_str)/death_global.csv ./data/
	cp ../coronaBreakSuck2020/data/raw/$(date_str)/recovered_global.csv ./data/
	cp ../coronaBreakSuck2020/data/raw/$(date_str)/conf_USA.csv ./data/
	cp ../coronaBreakSuck2020/data/raw/$(date_str)/death_USA.csv ./data/

image:
	docker build -t coronaBreakSuck2020Dash .