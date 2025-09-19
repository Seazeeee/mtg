from pathlib import Path
from dagster_dbt import DbtProject
import os
from dotenv import load_dotenv

load_dotenv()
DBT_PROFILES = os.getenv("DBT_PROFILES")

dbt_project = DbtProject(
    project_dir=str(Path("dbt_project").resolve()),
    profiles_dir=str(Path(DBT_PROFILES).resolve()),
)

dbt_project.prepare_if_dev()
