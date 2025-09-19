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

load_dotenv()
DB = os.getenv("DUCKDB_PATH")
DBT_PROFILES = os.getenv("DBT_PROFILES")

api_asset = load_assets_from_modules([api_call_store])

api_job = define_asset_job("api_job", selection=AssetSelection.all())

api_schedule = ScheduleDefinition(
    job=api_job,
    cron_schedule="@daily",
)

defs = Definitions(
    assets=api_asset,
    resources={
        "duckdb": DuckDBResource(database=str(DB)),
        "dbt": DbtCliResource(
            project_dir="/home/seaze/Projects/mtg-prod/mtg/dbt_project",
            profiles_dir=str(DBT_PROFILES),
        ),
    },
    schedules=[api_schedule],
)
