#!/usr/bin/env bash
set -euo pipefail

source hack/libraries/custom-logger.sh -v

if [ ! -f .env ]
then
    ewarn 'Environment ".env" file not found.'
    ewarn 'Creating using default settings from ".env.example."'
    cp .env.example .env
fi


set -o allexport
source .env
set +o allexport
eok 'Environment variables initialized'

docker compose up --detach --quiet-pull --remove-orphans
eok "PostgreSQL and Jager started"


python3 -m venv .venv/
source .venv/bin/activate
python3 -m pip install --upgrade pip --quiet
pip3 install -r requirements.txt --quiet
eok 'Pythond virtual environment initialized'


python3 tests/populate.py
eok 'database populated using "tests/integration/fakenames.csv" dataset'

eok 'Development environment successfully initialized'