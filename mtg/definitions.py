# Imports
import os
from dagster import (
    Definitions,
    load_assets_from_modules,
    ScheduleDefinition,
    define_asset_job,
    AssetSelection,
)
from dagster_duckdb import DuckDBResource
from dagster_dbt import DbtCliResource
from dotenv import load_dotenv

from .assets import api_call_store

# Get DB
load_dotenv()
DB = os.getenv("DUCKDB_PATH")

# Define asset
api_asset = load_assets_from_modules([api_call_store])

# Define job
api_job = define_asset_job("api_job", selection=AssetSelection.all())

# Define Schedule
api_schedule = ScheduleDefinition(
    job=api_job,
    cron_schedule="@daily",  # every day
)

# Dagster Definitions
defs = Definitions(
    assets=api_asset,
    resources={
        "duckdb": DuckDBResource(database=str(DB)),
        "dbt": DbtCliResource(project_dir="dbt_project"),
    },
    schedules=[api_schedule],
)
