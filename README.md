# MTG Data Engineering Project

This project is a personal exploration into the world of data engineering, using Magic: The Gathering (MTG) data from the Scryfall API. The goal is to create a fully local pipeline for extracting, transforming, and visualizing the data, using tools such as Python, DuckDB, Dagster, dbt, and Metabase. This project provides hands-on experience with data orchestration, database management, and data visualization.

## Project Overview

This project pulls data from the Scryfall API and stores it in a DuckDB database. From there, **Dagster** orchestrates the scheduling of data pipelines, while **dbt** handles data transformation. Finally, **Metabase** is used to visualize and access the data. Additionally, the project integrates with another API from the Commander Spellbook backend to explore infinite combos in Magic: The Gathering.

## Tech Stack

- **Python**: Used for data extraction and API integration.
- **DuckDB**: Lightweight local database to store and query the data.
- **Dagster**: Data orchestrator for scheduling and pipeline management.
- **dbt (Data Build Tool)**: For data transformation and modeling within the database.
- **Metabase**: BI tool for querying and visualizing the data.
- **Git**: Version control and CI/CD for the project.

## Project Status

### Completed

1. **API Integration**: Successfully pulled data from the [Scryfall API](https://scryfall.com/docs/api) and created tables in DuckDB.
2. **Historical Tracking**: Implemented a system to track historical changes in the data with a 7-day check to maintain freshness.

### In Progress

1. **Transformation with dbt**: Implementing dbt to perform transformations on the raw data before loading it into Metabase for visualization.
2. **Integration of Dagster and Metabase**: Working on running both Dagster and Metabase locally, ensuring smooth orchestration of data pipelines alongside accessible visualizations.
3. **Backend API for Infinite Combos**: Exploring integration with the [Commander Spellbook API](https://backend.commanderspellbook.com/) to link and analyze potential infinite combos in Magic: The Gathering.

## Next Steps

1. **Implement dbt Models**: Complete the dbt integration for cleaning and transforming the data.
2. **Dagster and Metabase Compatibility**: Ensure both systems can run concurrently and smoothly on a local setup.
3. **API Integration for Infinite Combos**: Enhance the data with infinite combo details from the Commander Spellbook API.

## How to Run

1. **Install Requirements**: Make sure you have Python, DuckDB, Dagster, dbt, and Metabase installed locally.
   ```
   pip install -e ".[dev]"
   ```
2. **Run the ETL Pipeline**: Use Dagster to orchestrate the pipeline.

   ```
   dagster dev
   ```

3. **Visualize Data**: Start Metabase to explore and visualize the data.

   ```
   cd ~/metabase
   java -jar metabase.jar
   ```

## Learnings and Reflections

This project has provided valuable insights into the end-to-end data engineering process, from data extraction via API to visualization. I’m developing a deeper understanding of **orchestration with Dagster**, **database management with DuckDB**, and **data transformations with dbt**. Metabase adds another layer of learning with its capabilities in visualizing and querying data.
