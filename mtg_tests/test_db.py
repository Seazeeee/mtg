import duckdb
import os
from dotenv import load_dotenv

if __name__ == "__main__":

    # Get DB
    load_dotenv()
    DB = os.getenv("DUCKDB_PATH")

    connection = duckdb.connect(DB)

    results = connection.execute("SHOW TABLES;").fetchall()
    print(connection.sql("SHOW TABLES"))
