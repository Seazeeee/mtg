import duckdb
import os
from dotenv import load_dotenv
from datetime import datetime

if __name__ == "__main__":

    # Get DB
    load_dotenv()
    DB = os.getenv("DUCKDB_PATH")

    connection = duckdb.connect(DB)

    results = connection.execute("SHOW TABLES;").fetchall()
    # connection.sql("DELETE FROM scryfall_data")
    print(connection.sql("SHOW TABLES"))
    print(connection.sql("SELECT count(*) FROM scryfall_data"))
    # print(
    #     connection.sql(
    #         """
    #         SELECT DISTINCT * FROM scryfall_data_10_22_2024 t
    #         WHERE NOT EXISTS (
    #             SELECT 1
    #             FROM scryfall_data sd
    #             WHERE CAST(sd.date AS DATE) = CAST(t.date AS DATE)

    #         )"""
    #     )
    # )
