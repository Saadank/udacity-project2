import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Loads data from S3 into staging tables on Redshift.
    
    Parameters:
    cur (cursor): Cursor to execute PostgreSQL commands in a database session.
    conn (connection): Connection to the PostgreSQL database.
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Inserts data from staging tables into the analytics tables on Redshift.
    
    Parameters:
    cur (cursor): Cursor to execute PostgreSQL commands in a database session.
    conn (connection): Connection to the PostgreSQL database.
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

def print_row_counts(cur):
    """Prints row counts for all tables to validate data load."""
    queries = [
        "SELECT COUNT(*) FROM staging_events;",
        "SELECT COUNT(*) FROM staging_songs;",
        "SELECT COUNT(*) FROM songplays;",
        "SELECT COUNT(*) FROM users;",
        "SELECT COUNT(*) FROM songs;",
        "SELECT COUNT(*) FROM artists;",
        "SELECT COUNT(*) FROM time;"
    ]
    
    for query in queries:
        cur.execute(query)
        result = cur.fetchone()
        print(f"{query} → {result[0]} rows")

def main():
    """Establishes connection to the Redshift cluster, loads data into staging tables,
    inserts data into analytics tables, and prints row counts for validation.
    """
    
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)
    print_row_counts(cur)

    conn.close()


if __name__ == "__main__":
    main()