# Data Warehouse ETL Pipeline - Sparkify

## Project Summary

This project implements an ETL pipeline to load and transform data for a fictional music streaming company, Sparkify, using AWS Redshift. The goal is to store log and song play data in a structured, star schema format for efficient querying and analysis.

## Dataset

The data comes from two S3 buckets:
- **Log Data**: Simulated user activity logs (s3://udacity-dend/log_data)
- **Song Data**: Metadata about songs (s3://udacity-dend/song_data)

A JSON file (s3://udacity-dend/log_json_path.json) is used to help parse log data into a structured format.

## Schema Design

The data is structured using a star schema with:

- **Fact Table**: `songplays` (records of song play events)
- **Dimension Tables**: `users`, `songs`, `artists`, `time`

## Files in This Repository

1. **Configuration File (`dwh.cfg`)**
   - Stores AWS Redshift cluster and IAM credentials.
   - Ensure this file is updated with the correct details before running the scripts.

2. **SQL Queries (`sql_queries.py`)**
   - Defines SQL statements for:
     - Table creation (`CREATE TABLE`)
     - Data loading from S3 (`COPY` commands)
     - Data insertion into analytics tables (`INSERT` statements)

3. **Table Creation Script (`create_tables.py`)**
   - Drops existing tables (if any) and recreates them.
   - Run this before executing the ETL pipeline to ensure a clean database.
   - **Run command**: `python create_tables.py`

4. **ETL Pipeline (`etl.py`)**
   - Loads data from S3 to Redshift.
   - Extracts data from staging tables into fact and dimension tables.
   - **Run command**: `python etl.py`

5. **Query Execution and Visualization (`query_runner.py`)**
   - Runs analytics queries on Redshift.
   - Generates visualizations using Matplotlib/Seaborn.
   - **Run command**: `python query_runner.py`

## How to Run the Project

1. **Setup AWS Redshift Cluster**
   - Ensure the Redshift cluster is running and the `dwh.cfg` file contains the correct IAM role and Redshift endpoint.
   - The IAM role should have `AmazonS3ReadOnlyAccess`.

2. **Create Tables**
   - Run command: `python create_tables.py`

3. **Run ETL Pipeline**
   - Run command: `python etl.py`

4. **Validate Data & Run Queries**
   - Run command: `python query_runner.py`

## Data Quality Checks

After running `etl.py`, verify the number of records in each table using:

```sql
SELECT COUNT(*) FROM staging_events;
SELECT COUNT(*) FROM staging_songs;
SELECT COUNT(*) FROM songplays;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM songs;
SELECT COUNT(*) FROM artists;
SELECT COUNT(*) FROM time;