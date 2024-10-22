import requests
import os
import duckdb
import pandas as pd
import pytz as tz
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dagster_duckdb import DuckDBResource
from dagster import asset, AssetExecutionContext, op, graph_asset
from dagster_dbt import DbtCliResource, dbt_assets

load_dotenv()
MF = str(os.getenv("MANIFEST_PATH"))


@asset(compute_kind="python")
def store_data(duckdb: DuckDBResource, get_pandas) -> None:
    """Store data in duck db"""

    # Define dataframe.
    df = get_pandas

    # Date Creation
    est = tz.timezone("America/New_York")

    current_time = datetime.now(est)

    date = current_time.strftime("%m_%d_%Y")

    # Connection string for duckdb
    with duckdb.get_connection() as connection:

        # Drop old tables

        # Fetch all the tables
        results = connection.execute("SHOW TABLES;").fetchall()

        # Grab Table Names
        tables = [r[0] for r in results]

        # Loop through
        for table in tables:
            if table.startswith("api_data"):
                dates = connection.execute(f"SELECT Date FROM {table};").fetchall()

                for single_date in dates:

                    # Step 1: Convert the date string to a datetime object
                    date_obj = datetime.strptime(single_date[0], "%m-%d-%Y")

                    # Step 2: Calculate the time difference between now and the table's date
                    time_diff = datetime.now() - date_obj

                    if time_diff > timedelta(days=1):
                        connection.execute(f"DROP TABLE {table}")

                    break

        # Create query
        query = f"CREATE OR REPLACE TABLE dbo.scryfall_data_{date} AS SELECT * FROM df;"

        # Pushing the df into the DB.
        connection.execute(query)


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

        oracle_card = [x for x in inside_data if x["type"] == "oracle_cards"]

        second_hit = requests.get(oracle_card[0]["download_uri"], timeout=60)

        # Grab the json
        data = second_hit.json()

        # Create dataframe
        df = pd.DataFrame(data)

        # Insert todays date

        est = tz.timezone("America/New_York")

        current_time = datetime.now(est)

        date = current_time.strftime("%m-%d-%Y")

        df.insert(0, "date", date)

        # Return the dataframe

        return df


@asset(deps=["fetch_api_data"], compute_kind="python")
def get_pandas():
    return fetch_api_data()


@dbt_assets(manifest=MF)
def dbt_test(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
