import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    
    Parameters:
    cur (cursor): Cursor to execute PostgreSQL commands in a database session.
    conn (connection): Connection to the PostgreSQL database.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list.
    
    Parameters:
    cur (cursor): Cursor to execute PostgreSQL commands in a database session.
    conn (connection): Connection to the PostgreSQL database.
    """

    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Establishes connection to the Redshift cluster, drops all tables, and creates all tables.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()