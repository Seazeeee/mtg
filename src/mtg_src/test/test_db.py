import duckdb
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

if __name__ == "__main__":

    # Get DB
    load_dotenv()
    DB = os.getenv("DUCKDB_PATH")

    connection = duckdb.connect(DB)

    # results = connection.execute("SHOW TABLES;").fetchall()
    print(connection.sql("SHOW TABLES"))

    # print(
    #     connection.sql(
    #         """
    #     WITH exploded_prices AS (
    #                 SELECT
    #                     date,
    #                     set,
    #                     name,
    #                     CAST(JSON_EXTRACT(prices, '$.usd') AS DOUBLE) AS nonfoil_price,
    #                     CAST(JSON_EXTRACT(prices, '$.usd_foil') AS DOUBLE) AS foil_price,
    #                     CAST(JSON_EXTRACT(prices, '$.usd_etched') AS DOUBLE) AS etched_price,
    #                     UNNEST(finishes) as finish,
    #                     rarity
    #                 FROM {{ source ('main', 'scryfall_data') }}
    #             )
    #             SELECT
    #             date,
    #             set,
    #             name,
    #             finish,
    #             CASE
    #                 WHEN finish LIKE '%nonfoil%' THEN nonfoil_price
    #                 WHEN finish LIKE '%foil%' THEN foil_price
    #                 WHEN finish LIKE '%etched%' THEN etched_price
    #             END AS price,
    #             rarity
    #             FROM exploded_prices
    #             WHERE price IS NOT NULL
    #             AND CAST(date AS DATE) = CAST(current_date() AS DATE)
    # """
    #     )
    # )
