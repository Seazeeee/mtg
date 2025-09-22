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
from mtg_src.assets import api_call_store
from pathlib import Path

load_dotenv()
BASE_DIR = Path.cwd()
CUR_DIR = Path(__file__).parent.parent.resolve()
DB = (BASE_DIR / Path(str(os.getenv("DUCKDB_PATH")))).resolve()
DBT_PROFILES = (CUR_DIR / Path(str(os.getenv("DBT")))).resolve()
DBT_DIR = (CUR_DIR / Path(str(os.getenv("DBT")))).resolve()

api_asset = load_assets_from_modules([api_call_store])

api_job = define_asset_job("api_job", selection=AssetSelection.all())

api_schedule = ScheduleDefinition(
    job=api_job,
    cron_schedule="*/15 * * * *",
)

defs = Definitions(
    assets=api_asset,
    resources={
        "duckdb": DuckDBResource(database=str(DB)),
        "dbt": DbtCliResource(
            project_dir=str(DBT_DIR),
            profiles_dir=str(DBT_PROFILES),
        ),
    },
    schedules=[api_schedule],
)
