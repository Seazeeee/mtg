from pathlib import Path

from dagster_dbt import DbtProject

dbt_project = DbtProject(
    project_dir=Path("dbt_project").resolve(),
)
# If `dagster dev` is used, the dbt project will be prepared to create the manifest at run time.
# Otherwise, we expect a manifest to be present in the project's target directory.
dbt_project.prepare_if_dev()
