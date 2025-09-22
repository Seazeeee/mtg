import os
from dotenv import load_dotenv
import duckdb

# Load environment variables from .env
load_dotenv()

# Path to the DuckDB file from environment variable
DB_PATH = str(os.getenv("DUCKDB_PATH"))

# Check if the file exists
if not os.path.exists(DB_PATH):
    print(f"{DB_PATH} does not exist. Creating DuckDB database...")
else:
    print(f"{DB_PATH} already exists. Using existing database.")

# Connect to DuckDB (will create the file if it doesn't exist)
con = duckdb.connect(DB_PATH)

# Optional: create a test table if you want
# con.execute("CREATE TABLE IF NOT EXISTS test(id INTEGER);")

con.close()
print("DuckDB database is ready.")
