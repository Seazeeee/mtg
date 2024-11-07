import requests
import os
import duckdb
import pandas as pd
import pytz as tz
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dagster_duckdb import DuckDBResource
from dagster import asset, AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

from mtg.project import dbt_project

load_dotenv()
MF = str(os.getenv("MANIFEST_PATH"))


@asset(compute_kind="python")
def store_data(duckdb: DuckDBResource, get_pandas):
    """Store data in duck db"""

    # Define dataframe.
    df = get_pandas

    # Date Creation
    est = tz.timezone("America/New_York")

    current_time = datetime.now(est)

    date = current_time.strftime("%m_%d_%Y")

    table_name = f"scryfall_data_{date}"

    # Connection string for duckdb
    with duckdb.get_connection() as connection:

        # Drop old tables

        # Fetch all the tables
        results = connection.execute("SHOW TABLES;").fetchall()

        # Grab Table Names
        tables = [r[0] for r in results]

        # Loop through
        for table in tables:

            if table.startswith("scryfall_data_"):

                date = table.split("_")[2:]

                table_date = datetime(int(date[-1]), int(date[0]), int(date[1]))

                compare = table_date + timedelta(days=15)

                if datetime.now() > compare:

                    connection.execute(f"DROP TABLE {table}")

        # Create query
        query = f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df;"

        # Pushing the df into the DB.
        connection.execute(query)

        # Insert into mass table
        connection.execute(
            f"""
            INSERT INTO scryfall_data
            SELECT DISTINCT * FROM {table_name} t
            WHERE NOT EXISTS (
                SELECT 1
                FROM scryfall_data sd
                WHERE CAST(sd.date AS DATE) = CAST(t.date AS DATE)
            )
            """
        )


@asset(compute_kind="python")
def fetch_api_data() -> pd.DataFrame:
    """Grab the json file from url"""

    # API Url
    URL = "https://api.scryfall.com/bulk-data"

    # Call the url
    response = requests.get(URL, timeout=60)

    # Check to make sure we have a good status
    if response.status_code == 200:

        first_splice = response.json()

        data_hit = [x for x in first_splice if x == "data"]

        inside_data = first_splice[data_hit[0]]

        oracle_card = [x for x in inside_data if x["type"] == "default_cards"]

        second_hit = requests.get(oracle_card[0]["download_uri"], timeout=60)

        # Grab the json
        data = second_hit.json()

        # Create dataframe
        df = pd.DataFrame(data)

        current_time = datetime.now()

        df.insert(0, "date", current_time)

        # Return the dataframe

        return df


@asset(deps=["fetch_api_data"], compute_kind="python")
def get_pandas():
    return fetch_api_data()


@asset(deps=["store_data"], compute_kind="python")
def date_check(duckdb: DuckDBResource):

    # Connection string for duckdb
    with duckdb.get_connection() as connection:
        connection.execute(
            "DELETE FROM scryfall_data WHERE CAST(date AS TIMESTAMP) < NOW() - INTERVAL 15 DAY;"
        )


@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_test(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
