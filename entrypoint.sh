#!/bin/bash

export PYTHONPATH=/app/src:$PYTHONPATH

set -x

python src/create_valid_db.py

dbt compile --project-dir $DBT_PATH

dagster-daemon run